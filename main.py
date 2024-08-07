from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI

from src.database import database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncContextManager[None]:
    database.connect()
    yield
    database.close()


app = FastAPI(lifespan=lifespan)


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=4526, reload=True, reload_dirs=["src"])


if __name__ == "__main__":
    main()
