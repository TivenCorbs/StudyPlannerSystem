#service3/main.py

import os
import httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlmodel import SQLModel, Field, Session, create_engine, select




#Start FASTAPI
app = FastAPI(title="Scheduling Services", version = "1.0.0")

engine = create_engine("sqlite:///scheduler.db")

#Pydantic Model

class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(index=True)
    message:str = "scheduled"


class ReminderCreate(SQLModel):
    task_id: int
    remind_at: datetime


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


@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)



#HealthCheck
@app.get("/health", response_model= HealthResponse)
async def health_check():
   dependencies = {}
   status = "healthy"

    #User Service HealthCheck
   try:
        
        start_time = time.time()
        res = httpx.get(f"{USER_SERVICE_URL}/health", timeout=3)
        dependencies["user-service"] = DependencyStatus(
        status="healthy" if res.status_code == 200 else "unhealthy",
        response_time_ms=int((time.time() - start_time) * 1000)
    )
   except Exception:
        dependencies["user-service"] = DependencyStatus(status="unhealthy")



   return HealthResponse(service = "scheduler-service", status="healthy",dependencies=dependencies)
    #Check Task Service

       

   



   #Checking User Service

