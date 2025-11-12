from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from sqlmodel import SQLModel, Field
from datetime import datetime
#Seperate database table known for Task service
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None

class TaskCreate(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


