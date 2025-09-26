from passlib.context import CryptContext
from pydantic import SecretStr

def hash_context():
    return CryptContext(schemes=["bcrypt", "argon2", "scrypt", "pbkdf2_sha256"], deprecated="auto")

def hash_password(password: SecretStr) -> str:
    pwd_context = hash_context()
    # Truncate password to 72 characters for bcrypt compatibility
    secret = password.get_secret_value()[:72]
    return pwd_context.hash(secret)

def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    pwd_context = hash_context()
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)