from app.database import sessionmanager
from sqlalchemy import select
from app.models import Image
import aiofiles.os
import aiofiles
import aiohttp
import asyncio
import os

from app.utils import (
    get_settings,
    chunkify,
    utcnow,
)


async def create_folder(path):
    if not await aiofiles.os.path.exists(path):
        try:
            await aiofiles.os.mkdir(path)
        except FileExistsError:
            pass


async def create_folders(path):
    folder_path = os.path.dirname(path)
    folders = folder_path.split("/")
    current_path = "/"

    for folder in folders:
        current_path = os.path.join(current_path, folder)
        await create_folder(current_path)

    return current_path


async def download(semaphore, session, image):
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as aio_session:
                async with aio_session.get(image.url) as r:
                    image_data = await r.read()

                    settings = get_settings()

                    system_path = settings.backend.system_path

                    save_path = f"{system_path}{image.local_path}"

                    await create_folders(save_path)

                    async with aiofiles.open(save_path, "wb") as f:
                        await f.write(image_data)

                    image.updated = utcnow()
                    image.downloaded = True
                    session.add(image)

                    print(f"Saved image {image.local_path}")

                    return True

        except aiohttp.ClientError:
            return False


async def download_images():
    async with sessionmanager.session() as session:
        semaphore = asyncio.Semaphore(50)

        images = await session.scalars(
            select(Image).filter(
                Image.downloaded == False,  # noqa: E712
            )
        )

        chunks_list = chunkify(images.all(), 100)

        for chunk in chunks_list:
            tasks = [download(semaphore, session, image) for image in chunk]

            await asyncio.gather(*tasks)

            await session.commit()
