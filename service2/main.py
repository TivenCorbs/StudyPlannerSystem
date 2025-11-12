import os
import httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel


#Initialize FastAPI
task_service = FastAPI(title="Task Services", version = "1.0.0")



#Setup environment in to connect with docker-compose.yml
#Completed updating docker compose along with the ports in the docker files


#It does this by looking up the variable on the docker compose


USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST", "user-service")


#No User Port? Assume Port:8001
USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT", 8001))


TASK_SERVICE_HOST = os.getenv("TASK_SERVICE_HOST","task-service")


#No User Port? Assume Port:8002
TASK_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT",8002))


#USER & TASK SERVICE URL: Connect to other services via correct address
USER_SERVICE_URL = f"https://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"

#Pydantic Model 

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
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