from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Добавляем схему авторизации
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Введите JWT-токен"
        }
    }

    # Применяем защиту ко всем операциям (или можно выборочно)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi