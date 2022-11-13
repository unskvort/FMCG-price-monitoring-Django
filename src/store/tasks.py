from typing import Literal

from celery import shared_task  # type: ignore

from parse.updater import Updater


@shared_task
def update_store() -> Literal[True]:
    updater = Updater()
    updater.run()
    return True
