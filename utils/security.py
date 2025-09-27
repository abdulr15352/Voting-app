from passlib.context import CryptContext
from pydantic import SecretStr
from jose import JWTError, jwt
from config import Settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from utils.constants import Endpoints, ResponseMessages
from v1.users.UserDBModels import get_user_by_email

settings = Settings()

def hash_context():
    return CryptContext(schemes=["bcrypt_sha256", "argon2", "scrypt", "pbkdf2_sha256"], deprecated="auto")

def hash_password(password: SecretStr) -> str:
    pwd_context = hash_context()
    secret = password.get_secret_value()
    return pwd_context.hash(secret)

def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    pwd_context = hash_context()
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)

def create_access_token(data: dict) -> str:
    encoded_jwt = jwt.encode(data, settings.JWT_SECRET_KEY.get_secret_value(), algorithm=settings.JWT_ALGORITHM)
    print("Encoded JWT:", encoded_jwt)  # Debugging line to print the token
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Endpoints.LOGIN)

def decode_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[settings.JWT_ALGORITHM])
        

        email = payload.get("email")
        if email is None:
            raise JWTError(status_code=401, detail=ResponseMessages.INVALID_TOKEN_MISSING_EMAIL)
        
        user = get_user_by_email(payload['email'])
        if user is None:
            raise JWTError(status_code=401, detail=ResponseMessages.USER_NOT_FOUND)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=ResponseMessages.INVALID_TOKEN) 