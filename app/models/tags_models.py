from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(unique=True)


