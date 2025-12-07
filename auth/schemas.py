from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="securepassword123", min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="securepassword123", min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIs...")
    token_type: str = Field(default="bearer", example="bearer")


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="Иванов Иван Иванович")
    bio: Optional[str] = Field(None, example="Программист, люблю писать код.")
    gender: Optional[str] = Field(None, example="male")
    profile_image_url: Optional[str] = Field(None, example="https://example.com/profile.jpg")

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v and v.lower() not in ('male', 'female', 'other'):
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else v

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Иванов Иван Иванович",
                "bio": "Программист, люблю писать код.",
                "gender": "male",
                "profile_image_url": "https://example.com/profile.jpg"
            }
        }

class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    bio: Optional[str]
    gender: Optional[str]
    profile_image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
