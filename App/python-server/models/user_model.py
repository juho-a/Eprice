from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from pydantic_core import PydanticCustomError
from typing import Optional
import re

class User(BaseModel):
    email: EmailStr  # Ensures the email is valid
    password: str
    role: Optional[str] = "user"  # Default role is "user"

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        # validate password strength (add more criteria as needed)
        assert len(password) >= 4, "Password must be at least 4 characters long"
        return password