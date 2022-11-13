import io
import time

import requests
from bs4 import BeautifulSoup
from django.core.files.images import ImageFile
from latest_user_agents import get_random_user_agent
from loguru import logger


class Downloader:
    def __init__(self) -> None:
        self.BASE_URL = "https://myspar.ru"
        self.POSTFIX = "?sort=rating"
        self.HEADERS = {"User-Agent": get_random_user_agent()}

    def _download(
        self,
        path: str | None = None,
        img: str | None = None,
        postfix: str | None = "",
        timeout: int = 10,
        requests_interval: int = 10,
        max_requests_number: int = 1,
    ) -> bytes | None:
        if img:
            url = img
        else:
            url = self.BASE_URL + path + postfix  # type: ignore
        for num_query in range(max_requests_number):
            try:
                request = requests.get(url, headers=self.HEADERS, timeout=timeout)
                if img and request.headers.get("content-type") == "image/webp":
                    return request.content
                elif request.headers.get("content-type") == "text/html; charset=UTF-8":
                    return request.content
            except Exception as e:
                logger.error(f"{e}")
                logger.info(f"A second request to the {url} will be sent in {requests_interval} seconds")
                time.sleep(requests_interval)
                continue
        return None

    def categories(self) -> list:
        categories: list[str] = []
        request = self._download(path="/catalog/")
        if request:
            soup = BeautifulSoup(request, "html.parser")
            links = soup.find_all(class_="section-tile__link")
            for link in links:
                categories.append(link.find(class_="js-cut-text").get("href"))
        return categories

    def products(self, category: str) -> dict[str, list[str]]:
        request = self._download(path=category, postfix=self.POSTFIX)
        soup = BeautifulSoup(request, "html.parser")  # type: ignore
        dataset: dict[str, list[str]] = {"title": [], "article": [], "image": [], "price": []}
        category_product = soup.find("meta", attrs={"name": "keywords"}).get("content")  # type: ignore
        products = soup.find_all(class_="catalog-list__item js-list-paging-item col-md-6 col-xl-4")

        for product in products:
            dataset["title"].append(product.find(class_="catalog-tile__name js-cut-text").text)
            dataset["article"].append(
                product.find(class_="catalog-tile__favorite js-favorite").get("data-item-article")
            )
            dataset["image"].append(product.source["data-srcset"])
            dataset["price"].append(product.find(class_="prices__cur js-item-price").text[:-4])
        dataset["category"] = [category_product] * len(dataset["title"])  # type: ignore
        return dataset

    def image(self, url: str, name: str) -> ImageFile:
        image_bytes = self._download(img=url)
        img = ImageFile(io.BytesIO(image_bytes), name=f"{name}.jpg")  # type: ignore
        return img
