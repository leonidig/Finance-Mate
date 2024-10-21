from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from .. import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int]
    name: Mapped[str]
    categories = relationship("Category", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship("User", back_populates="categories")