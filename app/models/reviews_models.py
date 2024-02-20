from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    description: Mapped[str]
    stars: Mapped[int]
    id_goods: Mapped[int] = mapped_column(ForeignKey("goods.id", ondelete="CASCADE"))
    name_user: Mapped[str] = mapped_column(
        ForeignKey("user.user_name", ondelete="CASCADE")
    )

    username_reviews: Mapped["User"] = relationship(back_populates="reviews")
    goods: Mapped["Goods"] = relationship(back_populates="reviews")

    # сделать удобо читаемый вид
    def str(self):
        return f"{self.title}"
