from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.schemas import (
    UserCreateModel, UserModel, UserLoginModel,
    ForgotPasswordConfirmModel, ForgotPasswordRequestModel, EmailModel
)
from auth.service import UserService
from auth.utils import generate_password_hash, create_access_token, decode_token, verify_password
from auth.dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user
from db.sql_main import get_session
from db.redis import add_jti_to_blocklist
from db.models import Users, PasswordResetOtp
from errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY_DAYS = 2
OTP_EXPIRATION_MINUTES = 10


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    html = "<h1>Welcome to MedCOCO Search</h1>"
    subject = "Welcome to MedCOCO Search"
    send_email.delay(emails.addresses, subject, html)
    return {"message": "Email sent successfully"}


@auth_router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)
async def create_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email 

    user_exist = await user_service.user_exists(email, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email already exists"
        )

    new_user = await user_service.create_user(user_data, session)

    access_token = create_access_token(
        user_data={
            "email": new_user.email,
            "user_uid": str(new_user.uid)
        }
    )

    refresh_token = create_access_token(
        user_data={
            "email": new_user.email,
            "user_uid": str(new_user.uid)
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    )

    subject = "Welcome to MedCOCO Search"
    html = f"""
    <h1>Welcome {new_user.email}</h1>
    <p>Thanks for signing up 🎉</p>
    """

    send_email.delay(
        [new_user.email],   # recipients
        subject,
        html
    )

    return JSONResponse(
        content={
            "message": "Signup successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": new_user.email,
                "uid": str(new_user.uid)
            }
        }
    )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    user = await user_service.get_user_by_email(login_data.email, session)

    if user is None or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)}
    )
    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)},
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    )

    return JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"email": user.email, "uid": str(user.uid)}
    })


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.post("/password-reset-request")
async def password_reset_request(
    email_data: ForgotPasswordRequestModel,
    session: AsyncSession = Depends(get_session)
):
    await user_service.create_password_reset_otp(email_data.email, session)
    return {"message": "OTP has been sent to your email"}


@auth_router.post("/password-reset-confirm")
async def reset_account_password(
    password_data: ForgotPasswordConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    if password_data.new_password != password_data.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    try:
        result = await session.exec(
            select(PasswordResetOtp).where(PasswordResetOtp.email == password_data.email)
        )
        stored_otp = result.first()

        if not stored_otp:
            raise HTTPException(status_code=400, detail="OTP expired or invalid")
        if stored_otp.otp != password_data.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if datetime.utcnow() > stored_otp.expires_at:
            await session.delete(stored_otp)
            await session.commit()
            raise HTTPException(status_code=400, detail="OTP expired")

        user_result = await session.exec(
            select(Users).where(Users.email == password_data.email)
        )
        user = user_result.first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password_hash = generate_password_hash(password_data.new_password)
        await session.delete(stored_otp)
        session.add(user)
        await session.commit()

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=status.HTTP_200_OK
    )


@auth_router.get("/me")
async def get_current_user_info(current_user: Users = Depends(get_current_user)):
    """Get the currently logged in user's info."""
    return {
        "uid": str(current_user.uid),
        "email": current_user.email,
        "username": current_user.username,
        "is_verified": current_user.is_verified
    }
    

