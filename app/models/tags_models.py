from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(unique=True)

    goods_tag = relationship("Goods", back_populates="tag")

    def __str__(self):
        return f"Тег: {self.tag}"
