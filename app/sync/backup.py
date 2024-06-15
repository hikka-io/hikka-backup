from app.utils import get_settings, utcnow
from app.database import sessionmanager
from sqlalchemy import select
from app.models import Image
from uuid import uuid4
import aiohttp


async def get_backup_images(page=1, size=100):
    settings = get_settings()

    endpoint = f"https://api.hikka.io/backup/images?page={page}&size={size}"

    async with aiohttp.ClientSession(
        headers={"Auth": settings.backend.token}
    ) as session:
        async with session.get(endpoint) as r:
            data = await r.json()
            return data


async def process_page(session, page):
    data = await get_backup_images(page)
    finished = False
    now = utcnow()

    print(f"Backing up images form page {page}")

    paths = [entry["path"] for entry in data["list"]]

    cache = await session.scalars(select(Image).filter(Image.path.in_(paths)))

    path_cache = {entry.path: entry for entry in cache}

    for entry in data["list"]:
        if path_cache.get(entry["path"]):
            finished = True
            continue

        image = Image(
            **{
                "local_path": entry["path"],
                "path": entry["path"],
                "downloaded": False,
                "updated": now,
                "created": now,
                "id": uuid4(),
            }
        )

        if len(image.local_path) > 255:
            extension = image.local_path.split(".")[-1]
            image.local_path = f"/long/{str(image.id)}.{extension}"
            image.updated = utcnow()

        session.add(image)

        print(f"Saved image {image.path}")

    return finished


async def backup_images():
    async with sessionmanager.session() as session:
        data = await get_backup_images()
        pages = data["pagination"]["pages"]

        finished = False

        for page in range(1, pages + 1):
            finished = await process_page(session, page)
            await session.commit()

            if finished:
                print("Found known image, stopping")
                break
