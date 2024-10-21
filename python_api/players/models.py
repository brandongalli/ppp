from pydantic import BaseModel, EmailStr
from user.models import UserResponseModel


class Player(BaseModel):
    first_name: str
    last_name: str
    team: str
    position: str
    height: str
    weight: str
    birth_year: int
    debut_year: int
    college: str
    bio: str



class SignUpRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class UserAuthResponseModel(BaseModel):
    token: TokenModel
    user: UserResponseModel


class AccessTokenResponseModel(BaseModel):
    access_token: str
