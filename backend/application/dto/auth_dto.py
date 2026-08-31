"""Auth DTOs."""

from dataclasses import dataclass


@dataclass
class LoginRequestDTO:
    email: str
    password: str


@dataclass
class RegisterRequestDTO:
    email: str
    password: str
    name: str
    surname: str = ""
    username: str = ""
    role: str = "PLAYER"


@dataclass
class TokenResponseDTO:
    access_token: str
    token_type: str
    user_id: str
    role: str
