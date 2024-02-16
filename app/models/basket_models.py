from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Base


class Basket(Base):
    __tablename__ = "basket"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_goods: Mapped[int] = mapped_column(ForeignKey("goods.id",ondelete="CASCADE"))
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id",ondelete="CASCADE"))