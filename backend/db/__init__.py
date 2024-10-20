import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///users.db", echo=True)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


class Base(DeclarativeBase):
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


from .models import User


asyncio.run(migrate())