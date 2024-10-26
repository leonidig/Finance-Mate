from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: Optional[int] = None
    name: str


class CategoryData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    total: float
    telegram_id: int


class GetAllCategories(BaseModel):
    telegram_id: int


class TransactionData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    category_title: str  
    amount: float