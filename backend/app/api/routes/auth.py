from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    credentials_valid = (
        form_data.username == settings.ADMIN_USERNAME
        and verify_password(
            form_data.password,
            settings.ADMIN_PASSWORD_HASH,
        )
    )

    if not credentials_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        subject=settings.ADMIN_USERNAME,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }