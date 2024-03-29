from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))
    image_path: Mapped[str] = mapped_column(Text, nullable=False)

    reviews: Mapped[list["Reviews"]] = relationship(back_populates="goods")
    # связать,чтобы было видно название тега
    # сделать удобо читаемый вид
    tag = relationship("Tags", back_populates="goods_tag")
    name_goods = relationship("Basket", back_populates="goods")

    def __str__(self):
        return f"Название товара: {self.title}"
