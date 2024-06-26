from app.database import sessionmanager
from app.utils import get_settings
import asyncio

from app.sync import (
    download_images,
    backup_images,
)


async def run_backup():
    settings = get_settings()
    sessionmanager.init(settings.database.endpoint)

    await backup_images()
    await download_images()

    await sessionmanager.close()


if __name__ == "__main__":
    asyncio.run(run_backup())
