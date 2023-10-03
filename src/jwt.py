from fastapi import Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Union
from datetime import datetime, timedelta
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src import exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_jwt(access_token: str = Cookie(default=None)) -> dict:
    if access_token is None:
        raise exceptions.CredentialsDataWrong()
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise exceptions.CredentialsDataWrong()
    except JWTError:
        raise exceptions.CredentialsDataWrong()
    return payload
