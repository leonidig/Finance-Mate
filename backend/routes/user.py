from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from .. import app
from ..db import (Session,
                  User,
                  Category,
                  Transaction)
from ..schemas import (UserData,
                       CategoryData,
                       GetAllCategories, 
                       TransactionData,
                       CreateChart)


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
    user = await session.scalar(
        select(User).where(User.telegram_id == data.telegram_id)
    )
    if not user:
        raise NotImplementedError()
    category = Category(title=data.title, user=user, total=data.total, telegram_id=data.telegram_id)
    session.add(category)

    return category


@app.get("/get_all_categories")
async def get_all(data: GetAllCategories, session=Depends(get_session)):
    user = await session.scalar(
        select(User).where(User.telegram_id == data.telegram_id)
    )

    if user:
        categories = await user.awaitable_attrs.categories
        return [{"id": category.id, "title": category.title} for category in categories]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/create_transaction", status_code=201)
async def create_transaction(transaction_data: TransactionData, session=Depends(get_session)):
    user = await session.scalar(select(User).where(User.telegram_id == transaction_data.telegram_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    category = await session.scalar(select(Category).where(Category.title == transaction_data.category_title, Category.user_id == user.id))

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    transaction = Transaction(
        telegram_id=transaction_data.telegram_id,
        category_title=transaction_data.category_title,
        category_id=category.id,
        amount=transaction_data.amount,
    )
    session.add(transaction)
    category.total += transaction_data.amount  
    session.add(category)

    return transaction


@app.get("/get_chart")
async def create_chart(data: CreateChart, session=Depends(get_session)):
    transactions = await session.scalars(select(Transaction).where(Transaction.telegram_id == data.telegram_id, Transaction.category_title == data.category_title).limit(10))
    transactions = [{"amount": transaction.amount} for transaction in transactions]
    return transactions


@app.get("/get_chart_by_total")
async def get_chart_by_total(data: GetAllCategories, session=Depends(get_session)):
    user = await session.scalar(select(User).where(User.telegram_id == data.telegram_id))
    categories = await session.scalars(select(Category).where(Category.user_id == user.id))
    totals = [{category.title : category.total} for category in categories]
    return totals


@app.delete("/delete_category/{category_name}")
async def delete_category(category_name, data: CreateChart, session=Depends(get_session)):
    category = await session.scalar(select(Category).where(Category.title == data.category_title))
    if category.telegram_id != data.telegram_id:
        return "Permission Denied"
    else:
        await session.delete(category)
