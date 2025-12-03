from fastapi import FastAPI
from auth.router import router as auth_router
from db.base import Base
from db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="По следам — Auth Service",
    description="Микросервис аутентификации для мобильного приложения «По следам»",
    version="1.0.0",
    docs_url="/auth/docs",
    redoc_url="/auth/redoc",
    openapi_url="/auth/openapi.json",
)

app.include_router(auth_router)
