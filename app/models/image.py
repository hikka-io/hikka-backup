from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class Image(Base):
    __tablename__ = "service_images"

    path: Mapped[str] = mapped_column(unique=True, index=True)
    downloaded: Mapped[bool] = mapped_column(default=False)
    local_path: Mapped[str] = mapped_column(nullable=True)
    updated: Mapped[datetime]
    created: Mapped[datetime]

    @hybrid_property
    def url(self):
        return "https://cdn.hikka.io" + self.path
