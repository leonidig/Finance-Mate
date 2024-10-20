from sqlalchemy import select
from fastapi import HTTPException
from aiohttp import ClientSession
from .. import app
from ..db import Session, User
from ..schemas import UserData

    
    
@app.post("/create_user", status_code=201)
async def create_user(data: UserData):
    try:
        async with Session.begin() as session:
            user = User(**data.model_dump())
            session.add(user)
    except:
        raise HTTPException(400, detail="User already exist")