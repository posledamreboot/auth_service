from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.schemas import UserCreate, UserLogin, Token
from auth.crud import get_user_by_email, create_user
from auth.utils import verify_password
from core.security import create_access_token
from auth.deps import get_db, get_current_user
from auth.models import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description=(
        "Создаёт нового пользователя в системе и сразу возвращает JWT-токен. "
        "Email должен быть уникальным."
    ),
    response_description="Успешная регистрация и токен доступа"
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        new_user = create_user(db, user)
        access_token = create_access_token(data={"sub": str(new_user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to internal error"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему",
    description=(
        "Аутентифицирует пользователя по email и паролю. "
        "Возвращает JWT-токен при успешной проверке."
    ),
    response_description="Токен доступа при успешной аутентификации"
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users",
    summary="Получить список всех пользователей",
    description=(
        "Возвращает список всех зарегистрированных пользователей (только id и email). "
        "Доступен только авторизованным пользователям."
    ),
    response_description="Список пользователей"
)
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email} for u in users]