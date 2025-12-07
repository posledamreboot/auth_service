from fastapi import FastAPI
from auth.routers.auth import router as auth_router
from auth.routers.user import router as user_router
from db.base import Base
from db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="По следам — User & Auth Service",
    description="Микросервис аутентификации и управления пользователями для мобильного приложения «По следам»",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth_router)
app.include_router(user_router)
