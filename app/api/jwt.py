from datetime import timedelta
from typing import Optional
import logging

from fastapi import Security, Header
from fastapi.exceptions import HTTPException

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer, JwtAuthorizationCredentials
from fastapi_jwt.jwt_backends.python_jose_backend import PythonJoseJWTBackend

from common.settings import settings

python_jose_jwt_backend = PythonJoseJWTBackend()

access_security = JwtAccessBearer(
    secret_key=settings.jwt_secret_key,
    access_expires_delta=timedelta(minutes=settings.access_expires_delta),
    auto_error=False
)

refresh_security = JwtRefreshBearer(
    secret_key=settings.jwt_secret_key,
    refresh_expires_delta=timedelta(days=settings.refresh_expires_delta),
    auto_error=False
)


async def get_jwt_token(
        jwt_token: Optional[str] = Header(..., description="Only jwt token"),
        credentials: Optional[JwtAuthorizationCredentials] = Security(access_security),
) -> dict:
    """Получает JWT-токен из заголовка Authorization или из OAuth2 (Swagger UI)."""
    token = None

    if credentials:
        return credentials  # Если токен передан через Security(access_security)

    if jwt_token:
        try:
            credentials = python_jose_jwt_backend.decode(token=jwt_token, secret_key=settings.jwt_secret_key)
            return credentials['subject']
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=401, detail=str(e))

    if not token:
        raise HTTPException(status_code=401, detail="Credentials are not provided")


async def refresh_jwt_token(
    refresh_token: Optional[str] = Header(..., description="Only refresh token"),
    credentials: Optional[JwtAuthorizationCredentials] = Security(refresh_security),
):
    token = None

    if credentials:
        return credentials  # Если токен передан через Security(access_security)

    if refresh_token:
        try:
            credentials = python_jose_jwt_backend.decode(token=refresh_token, secret_key=settings.jwt_secret_key)
            return credentials['subject']
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=401, detail=str(e))

    if not token:
        raise HTTPException(status_code=401, detail="Credentials are not provided")


async def get_jwt_token(
        jwt_token: Optional[str] = Header(..., description="jwt only"),
        credentials: Optional[JwtAuthorizationCredentials] = Security(access_security)
) -> dict:
    token = None

    if credentials:
        return credentials

    if jwt_token:
        try:
            credentials = python_jose_jwt_backend.decode(token=jwt_token, secret_key=settings.jwt_secret_key)
            return credentials['subject']
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=401, detail=str(e))

    if not token:
        raise HTTPException(status_code=401, detail="Credentials are not provided")
