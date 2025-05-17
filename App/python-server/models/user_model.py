from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from pydantic_core import PydanticCustomError
from typing import Optional
import re

class UserCode(BaseModel):
    email: EmailStr
    code: str

    @field_validator('code')
    def validate_code(cls, code: str) -> str:
        # validate code format (3 letters, dash, 3 digits)
        pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(pattern, code):
            raise PydanticCustomError("Invalid code format. Expected format: ABC-123")
        return code

class User(BaseModel):
    email: EmailStr  # Ensures the email is valid
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        # validate password strength (add more criteria as needed)
        assert len(password) >= 4, "Password must be at least 4 characters long"
        return password