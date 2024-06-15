from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import sessionmanager
from app.utils import get_settings
import asyncio

from app.sync import (
    download_images,
    backup_images,
)


def init_scheduler():
    scheduler = AsyncIOScheduler()
    settings = get_settings()
    sessionmanager.init(settings.database.endpoint)

    scheduler.add_job(download_images, "interval", hours=1)
    scheduler.add_job(backup_images, "interval", hours=1)
    scheduler.start()

    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        loop.run_until_complete(sessionmanager.close())
        loop.close()


if __name__ == "__main__":
    init_scheduler()
