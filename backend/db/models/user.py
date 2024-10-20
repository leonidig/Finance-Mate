from sqlalchemy.orm import Mapped
from .. import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int]
    name: Mapped[str]