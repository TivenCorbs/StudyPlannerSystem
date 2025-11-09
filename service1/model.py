from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from sqlmodel import SQLModel, Field

class User_Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str


class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]


class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]

