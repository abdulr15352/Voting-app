from passlib.context import CryptContext
from pydantic import SecretStr
from jose import JWTError, jwt
from config import Settings

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

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY.get_secret_value(), algorithm=[settings.JWT_ALGORITHM])
        print("Decoded Payload:", payload)  # Debugging line to print the payload
        return payload
    except JWTError:
        return None