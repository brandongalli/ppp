from sqlmodel import SQLModel, Field
from typing import Optional

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    first_name: str = Field(default=None, nullable=False)
    last_name: str = Field(default=None, nullable=False)
    team: str = Field(default=None, nullable=False)
    position: str = Field(default=None, nullable=False)
    height: str = Field(default=None, nullable=False)
    weight: str = Field(default=None, nullable=False)
    birth_year: int = Field(default=None, nullable=False)
    debut_year: int = Field(default=None, nullable=False)
    college: str = Field(default=None, nullable=False)
    bio: str = Field(default=None, nullable=False)
