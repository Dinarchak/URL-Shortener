from fastapi import FastAPI
from routes import router
from contextlib import asynccontextmanager
from database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    

app = FastAPI(lifespan=lifespan)
app.include_router(router)
