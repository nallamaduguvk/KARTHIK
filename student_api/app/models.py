from pydantic import BaseModel, EmailStr, Field, validator
import re

phone_regex = re.compile(r"^\d{10}$")

class StudentBase(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    grade: str = Field(..., example="10")
    age: int = Field(..., ge=1, example=15)
    phone_number: str = Field(..., example="1234567890")
    email: EmailStr = Field(..., example="john@example.com")
    address: str = Field(..., example="123 Main St")
    father_name: str = Field(..., example="Father Name")
    mother_name: str = Field(..., example="Mother Name")

    @validator("phone_number")
    def validate_phone(cls, v: str) -> str:
        if not phone_regex.match(v):
            raise ValueError("phone number must be 10 digits")
        return v

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: str
