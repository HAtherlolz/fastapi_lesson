import json
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator


class CreateProfile(BaseModel):
    """ Schema for profiles validation  """
    avatar: str | None = Field(example="blob:https://web.telegram.org/355df984-f60c-4f2c-9d3b-c02d5431a9dd")
    email: EmailStr
    password: str = Field(description="The profiles password", max_length=255, min_length=8)
    first_name: str = Field(example="Ivan")
    last_name: str | None = Field(example="Chelovek")
    lat: float | None = Field(example=46.9659100)
    lng: float | None = Field(example=31.9974000)
    country: str | None = Field(example="Ukraine")
    city: str | None = Field(example="Nikolaev")

    class Config:
        orm_mode = True
        # schema_extra = {
        #     "example": {
        #         "first_name": "Jane Doe",
        #         "email": "jdoe@example.com"
        #     }
        # }

    @validator('first_name')
    def check_firstname(cls, v):
        if len(v) > 25:
            raise ValueError("The first_name len error")
        return v


class UpdateProfile(BaseModel):
    avatar: str | None = Field(example="blob:https://web.telegram.org/355df984-f60c-4f2c-9d3b-c02d5431a9dd")
    email: EmailStr | None
    first_name: str | None = Field(example="Ivan")
    last_name: str | None = Field(example="Chelovek")
    lat: float | None = Field(example=46.9659100)
    lng: float | None = Field(example=31.9974000)
    country: str | None = Field(example="Ukraine")
    city: str | None = Field(example="Nikolaev")

    class Config:
        orm_mode = True


class GetProfile(BaseModel):
    """ Schema for profile creation  """
    id: int
    avatar: str | None
    email: EmailStr
    first_name: str
    last_name: str | None
    lat: float | None
    lng: float | None
    country: str | None
    city: str | None
    date_joined: datetime

    class Config:
        orm_mode = True


class Test(BaseModel):
    id: int = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
