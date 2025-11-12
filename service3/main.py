#service3/main.py

import os
import httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlmodel import SQLModel,Field 
app = FastAPI(title="Scheduling Services", version = "1.0.0")








#Pydantic Model

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



#Describes status of single dependency
class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]

#Describes overall health status of service (similar to other services) 
class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]




#It does this by looking up the variable on the docker compose

USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST", "user-service")

#No User Port? Assume Port:8001
USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT", 8001))


TASK_SERVICE_HOST = os.getenv("TASK_SERVICE_HOST","task-service")
TASK_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT",8002))

#USER & TASK SERVICE URL: Connect to other services via correct address
USER_SERVICE_URL = f"https://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"
TASK_SERVICE_URL = f"https://{TASK_SERVICE_HOST}:{TASK_SERVICE_PORT}"


@app.get("/")
def root():
    return {"Message": "User Service is Running"}


