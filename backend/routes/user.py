from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from .. import app
from ..db import Session, User, Category
from ..schemas import UserData, CategoryData, GetAllCategories



@app.post("/create_user", status_code=201)
async def create_user(data: UserData):
    with Session.begin() as session:
        user = User(**data.model_dump())
        session.add(user) 
        return user

@app.post("/create_category", status_code=201)
async def create_category(data: CategoryData):
    with Session.begin() as session:
        category = Category(**data.model_dump())
        session.add(category)
        return category 

@app.get("/get_all_categories")
async def get_all(data: GetAllCategories):
    with Session.begin() as session:
        user = await session.scalar(select(User).where(User.telegram_id == data.user_id))
        if user:
            categories = user.categories
            return [{"id": category.id, "title": category.title} for category in categories]
        else:
            raise HTTPException(status_code=404, detail="User not found")
