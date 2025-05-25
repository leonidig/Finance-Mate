import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    # AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)

# from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    # sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
)


engine = create_async_engine("sqlite+aiosqlite:///mydb.db", echo=True)
Session = async_sessionmaker(
    engine, expire_on_commit=False
)  # sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


async def up():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def down():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def migrate():
    await down()
    await up()


from .models import User, Category, Transaction

asyncio.run(migrate())
