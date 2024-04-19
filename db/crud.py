from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db import models, schemas


class UserRepository:
    @classmethod
    async def get_user(cls, session: AsyncSession, username: str):
        query = select(models.User).filter_by(username=username)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        query = select(models.User).filter_by(email=email)
        result = await session.execute(query)
        return result.scalars().first()

    # @classmethod
    # async def get_user_by_referral_code(cls, session: AsyncSession, referral_code: str):
    #     query = select(models.User).join(models.ReferralCode).filter_by()

    @classmethod
    async def create_user(cls, session: AsyncSession, user_data: schemas.UserCreate):
        db_user = models.User(**user_data.model_dump())
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @classmethod
    async def create_referral_user(
        cls, session: AsyncSession, referral_user: models.User, referrer_id: int
    ):
        query = (
            select(models.User)
            .filter_by(id=referrer_id)
            .options(joinedload(models.User.referral))
        )
        result = await session.execute(query)
        referrer = result.scalars().first()
        if referrer:
            referrer.referral.append(referral_user)
            await session.commit()
            await session.refresh(referrer)
            return referrer


class ReferralCodeRepository:
    @classmethod
    async def get_code(cls, session: AsyncSession, referral_code: str):
        query = select(models.ReferralCode).filter_by(code=referral_code)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_code_by_user(cls, session: AsyncSession, user_id: int):
        query = select(models.ReferralCode).filter_by(user_id=user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_code_by_user_email(cls, session: AsyncSession, email: EmailStr):
        query = select(models.ReferralCode).join(models.User).filter_by(email=email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def create_code(
        cls, session: AsyncSession, code_data: schemas.ReferralCodeCreate, user_id: int
    ):
        db_code = models.ReferralCode(user_id=user_id, **code_data.model_dump())
        session.add(db_code)
        await session.commit()
        await session.refresh(db_code)
        return db_code
