from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChangeBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    environment: str = Field(min_length=1, max_length=50)
    status: str = Field(min_length=1, max_length=50)


class ChangeCreate(ChangeBase):
    pass


class ChangeResponse(ChangeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
