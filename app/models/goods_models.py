from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))

    reviews: Mapped[list["Reviews"]] = relationship(back_populates="goods")

