import random
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models import Users, PasswordResetOtp
from auth.schemas import UserCreateModel
from auth.utils import generate_password_hash
from celery_tasks import send_email

OTP_EXPIRATION_MINUTES = 10


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        result = await session.exec(select(Users).where(Users.email == email))
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = Users(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(self, user: Users, user_data: dict, session: AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)
        await session.commit()
        return user

    async def create_password_reset_otp(self, email: str, session: AsyncSession) -> None:
        user = await self.get_user_by_email(email, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete old OTPs for this email
        result = await session.exec(
            select(PasswordResetOtp).where(PasswordResetOtp.email == email)
        )
        for old_otp in result.all():
            await session.delete(old_otp)

        otp_code = str(random.randint(100000, 999999))
        otp_entry = PasswordResetOtp(
            email=email,
            otp=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRATION_MINUTES)
        )
        session.add(otp_entry)
        await session.commit()

        send_email.delay(
            email,
            "Your Password Reset OTP",
            f"<h1>Reset Your Password</h1><p>Your OTP is: <b>{otp_code}</b></p><p>Expires in {OTP_EXPIRATION_MINUTES} minutes.</p>"
        )
