from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_id")
    task_id: int = Field(foreign_key="task.id")
    remind_at: datetime
    message:str


class ReminderCreate(SQLModel):
    user_id: int
    task_id: int
    remind_at: datetime
    message: str


class ReminderResponse(SQLModel):
    user_id: int
    task_id: int
    remind_at: datetime
    message: str



