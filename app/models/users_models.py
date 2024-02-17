from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(length=320), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    review: Mapped["Reviews"] = relationship(back_populates="user_reviews")
