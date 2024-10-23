from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from .. import app
from ..db import Session, User, Category
from ..schemas import UserData, CategoryData, GetAllCategories


async def get_session():
    async with Session.begin() as session:
        yield session


@app.post("/create_user", status_code=201)
async def create_user(data: UserData, session=Depends(get_session)):
    user = User(**data.model_dump())
    session.add(user)
    return user


@app.post("/create_category", status_code=201)
async def create_category(data: CategoryData, session=Depends(get_session)):
    category = Category(**data.model_dump())
    session.add(category)

    return category


@app.get("/get_all_categories")
async def get_all(data: GetAllCategories, session=Depends(get_session)):
    categories = await session.scalars(
        select(Category)
        .join(User, Category.user_id == User.telegram_id)
        .where(User.telegram_id == data.user_id)
    )
    if categories:
        return [{"id": category.id, "title": category.title} for category in categories]
    else:
        raise HTTPException(status_code=404, detail="User not found")
