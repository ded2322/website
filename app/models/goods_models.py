from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey,Text,String

from app.database import Base


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100),unique=True)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))
    image_path:Mapped[str] = mapped_column(Text,nullable=False)

    reviews: Mapped[list["Reviews"]] = relationship(back_populates="goods")

