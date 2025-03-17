from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import upload, auth
from database import engine
from models import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables if not exists
    await init_db()
    yield


app = FastAPI(title="Fruit Detection API", version="1.0", lifespan=lifespan)

app.include_router(upload.router, prefix="/uploads", tags=["Uploads"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "Hello World!"}
