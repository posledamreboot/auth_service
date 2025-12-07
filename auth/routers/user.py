from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.crud import update_user_profile, delete_user
from auth.deps import get_db, get_current_user
from auth.models import User
from auth.schemas import UserProfileUpdate, UserProfile

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Получить свой профиль",
    description="Возвращает информацию о текущем аутентифицированном пользователе."
)
def read_own_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch(
    "/me",
    response_model=UserProfile,
    summary="Обновить свой профиль",
    description="Позволяет пользователю обновить свои данные: ФИО, о себе, пол, фото."
)
def update_own_profile(
        profile_update: UserProfileUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    updated_user = update_user_profile(db, current_user.id, profile_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить свой аккаунт",
    description="Позволяет пользователю удалить свой аккаунт."
)
def delete_own_account(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    success = delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return # 204 No Content