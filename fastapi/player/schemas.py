from pydantic import field_validator, ValidationInfo, BaseModel
from datetime import datetime
from player.models import PositionChoices, PlayerBase

class TeamCreate(BaseModel):
    """
    Model for creating a new team with validation on required fields.
    
    Attributes:
    - name: The name of the team.
    - logo_uri: URI for the team logo.
    """
    name: str
    logo_uri: str

    @field_validator('logo_uri')
    def check_logo_uri(cls, value: str, info: ValidationInfo) -> str:
        """
        Validates the logo URI. Add specific checks if needed, such as format or domain.
        
        Parameters:
        - value: The logo URI to validate.

        Returns:
        - The validated logo URI.
        """
        # Add additional validations if necessary (e.g., URL format check)
        return value

class PlayerCreate(PlayerBase):
    """
    Model for creating a new player with extensive validation.

    Validates:
    - first_name and last_name as alphanumeric.
    - position as one of the choices in PositionChoices.
    - height and weight as positive floats.
    - birth_year and debut_year as valid years within reasonable bounds.
    """

    @field_validator('first_name', 'last_name')
    def check_alphanumeric(cls, value: str, info: ValidationInfo) -> str:
        """
        Ensures that first and last names contain only alphanumeric characters and spaces.

        Parameters:
        - value: The name to validate.

        Returns:
        - The validated name if it passes checks.
        
        Raises:
        - AssertionError if the value is not alphanumeric.
        """
        if isinstance(value, str):
            is_alphanumeric = value.replace(' ', '').isalnum()
            assert is_alphanumeric, f'{info.field_name} must be alphanumeric'

        return value

    @field_validator('position')
    def position_must_be_valid(cls, value: str) -> str:
        """
        Validates the player's position against predefined PositionChoices.

        Parameters:
        - value: The position value to validate.

        Returns:
        - The validated position if it's valid.

        Raises:
        - ValueError if the position is not within PositionChoices.
        """
        if value not in PositionChoices:
            valid_positions = [choice.value for choice in PositionChoices]
            raise ValueError(f"Position must be one of: {valid_positions}")

        return value

    @field_validator('height', 'weight')
    def validate_height_weight(cls, value: float) -> float:
        """
        Validates that height and weight are positive numeric values.

        Parameters:
        - value: The height or weight value to validate.

        Returns:
        - The validated value if it is positive and numeric.

        Raises:
        - ValueError if the value is non-numeric or not greater than zero.
        """
        if not isinstance(value, (float, int)):
            raise ValueError("Value must be a numeric value.")
        if value <= 0:
            raise ValueError("Value must be greater than zero.")
        return float(value)

    @field_validator('birth_year', 'debut_year')
    def check_valid_year(cls, value: int, info: ValidationInfo) -> int:
        """
        Validates that birth and debut years are within a reasonable range.

        Parameters:
        - value: The year to validate.

        Returns:
        - The validated year if it is within the range.

        Raises:
        - ValueError if the year is outside the acceptable range (1900 to the current year).
        """
        current_year = datetime.now().year

        if not isinstance(value, int) or value < 0:
            raise ValueError("Year must be a non-negative integer.")
        if value < 1900 or value > current_year:
            raise ValueError(f"Year must be between 1900 and {current_year}.")
        return value
