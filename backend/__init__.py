from fastapi import FastAPI
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve



app = FastAPI(debug=True)

config = Config()
config.bind = ["localhost:8080"]


from . import routes


def main() -> None:
    asyncio.run(serve(app, config))