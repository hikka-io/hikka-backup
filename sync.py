from app.database import sessionmanager
from app.sync import download_images
from app.utils import get_settings
from app.sync import backup_images
import asyncio


async def test():
    settings = get_settings()
    sessionmanager.init(settings.database.endpoint)

    await backup_images()
    await download_images()

    await sessionmanager.close()


if __name__ == "__main__":
    asyncio.run(test())
