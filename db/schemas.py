from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from routes import referral


class ReferralCodeCreate(BaseModel):
    code: str
    description: Optional[str] = None
    expires_at: datetime

    @field_validator("expires_at")
    def validate_position(cls, date):
        if date < datetime.now():
            raise ValueError("Expiration date can't be less than now!")
        return date


class ReferralCodeDB(ReferralCodeCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserReferralDB(UserDB):
    referral: Optional[list["UserDB"]]


class UserAuth(BaseModel):
    id: int
    username: str
