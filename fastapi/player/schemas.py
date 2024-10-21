from pydantic import BaseModel

# Schema for reading users
class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Schema for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
