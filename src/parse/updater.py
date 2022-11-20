import pandas as pd
from django.db import transaction
from loguru import logger
from tqdm import tqdm

from parse.download import Downloader
from acus_store.models import Category, PriceRecord, Product


class Updater:
    def __init__(self) -> None:
        self.downloader = Downloader()
        self.df = pd.DataFrame()

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df.drop_duplicates(subset=["article"], inplace=True)
        df = df[df["title"].str.contains("SPAR") == False]  # noqa
        df.reset_index(drop=True, inplace=True)
        df["article"] = df["article"].astype("int64")
        df["price"] = df["price"].apply(lambda x: x.replace(" ", ""))
        df["price"] = df["price"].astype("int64")

        return df

    def update_store(self) -> pd.DataFrame:
        categories = self.downloader.categories()

        for category in tqdm(categories):
            try:
                tmp_df = pd.DataFrame(self.downloader.products(category))
                self.df = pd.concat([self.df, tmp_df])
            except Exception as e:
                logger.error(f"{e}, on {category}")
                continue

        self.df = self.clean_dataframe(self.df)
        return self.df

    @transaction.atomic
    def upload_to_db(self, dataset: pd.DataFrame) -> None:
        for i, row in dataset.iterrows():
            category, create_flag = Category.objects.get_or_create(name=row.category)
            product, create_flag = Product.objects.get_or_create(
                article=row.article, name=row.title, category=category, price=row.price
            )
            PriceRecord.objects.create(product=product, price=row.price)

            if not product.image:
                image = self.downloader.image(row.image, row.article)
                product.image = image  # type: ignore
            product.price = row.price
            product.save()
        logger.info(f"Store updated on {len(dataset)} products")

    def run(self) -> None:
        self.update_store()
        self.upload_to_db(self.df)
