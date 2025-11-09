from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: str

class userCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


#Health Model - Health Endpoint checks and responses
class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]


class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]