from typing import Union
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import ReferralCodeRepository
from db.database import get_session
from db.schemas import ReferralCodeCreate, ReferralCodeDB, UserAuth
from security.security import get_user_from_token


referralrouter = APIRouter()


@referralrouter.get("/code/", response_model=ReferralCodeDB)
async def get_my_code(
    session: AsyncSession = Depends(get_session),
    user_auth: UserAuth = Depends(get_user_from_token),
):
    user_id = user_auth.id
    code = await ReferralCodeRepository.get_code_by_user(session, user_id)
    if code:
        return code
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="You dont have any codes!"
    )


@referralrouter.get("/get_code/", response_model=ReferralCodeCreate)
async def get_referral_code_by_email(
    email: EmailStr, session: AsyncSession = Depends(get_session)
):
    code = await ReferralCodeRepository.get_code_by_user_email(session, email)
    return code


@referralrouter.post("/code/", response_model=ReferralCodeDB)
async def create_referral_code(
    code_data: ReferralCodeCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    user_auth: UserAuth = Depends(get_user_from_token),
):
    user_id = user_auth.id
    code = await ReferralCodeRepository.get_code_by_user(session, user_id)
    if code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have referral code!",
        )
    code = await ReferralCodeRepository.create_code(session, code_data, user_id)
    return code


@referralrouter.put("/code/", response_model=ReferralCodeDB)
async def update_referral_code(
    new_code_data: ReferralCodeCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    user_auth: UserAuth = Depends(get_user_from_token),
):
    user_id = user_auth.id
    code = await ReferralCodeRepository.get_code_by_user(session, user_id)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have code to update!",
        )
    code = await ReferralCodeRepository.update_code(session, code, new_code_data)
    return code
