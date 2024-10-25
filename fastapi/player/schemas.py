from pydantic import field_validator, ValidationInfo, BaseModel
from datetime import datetime
from player.models import PositionChoices, PlayerBase

class TeamCreate(BaseModel):
    name: str
    logo_uri: str

    @field_validator('logo_uri')
    def check_logo_uri(cls, value: str, info: ValidationInfo) -> str:
        
        return value

class PlayerCreate(PlayerBase):
    @field_validator('first_name', 'last_name')
    def check_alphanumeric(cls, value: str, info: ValidationInfo) -> str:
        if isinstance(value, str):
            is_alphanumeric = value.replace(' ', '').isalnum()
            assert is_alphanumeric, f'{info.field_name} must be alphanumeric'

        return value
    
    @field_validator('position')
    def color_must_be_valid(cls, value: str) -> str:
        if value not in PositionChoices:
            raise ValueError(f"Position must be one of: {[choice.value for choice in PositionChoices]}")

        return value

    @field_validator('height', 'weight')
    def validate_height_weight(cls, value):
        if not isinstance(value, float):
            raise ValueError("Value must be a numeric value.")
        if value <= 0:
            raise ValueError("Value must be greater than zero.")
        return value
    
    @field_validator('birth_year', 'debut_year')
    def check_valid_year(cls, value: str, info: ValidationInfo) -> str:
        current_year = datetime.now().year

        if not isinstance(value, int) or int(value) < 0:
            raise ValueError("Year must be a non-negative integer.")
        year = int(value)
        if year < 1900 or year > current_year:
            raise ValueError(f"Year must be between 1900 and {current_year}.")
        return year