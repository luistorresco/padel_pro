"""Auth service - JWT and password hashing domain logic."""

import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta


class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60 * 24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def create_access_token(self, user_id: str, role: str) -> str:
        to_encode = {
            "sub": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=self.expire_minutes),
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None
