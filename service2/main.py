#service2/main.py
import os
import httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel

#Initialize FastAPI
task_service = FastAPI(title="Task Services", version = "1.0.0")



#Setup environmentin to connect with docker-compose.yml

#It does this by looking up the variable on the docker compose

USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST", "user-service")

#No User Port? Assume Port:8001
USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT", 8001))

TASK_SERVICE_HOST = os.getenv("TASK_SERVICE_HOST","task-service")
TASK_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT",8002))

#USER & TASK SERVICE URL: Connect to other services via correct address
USER_SERVICE_URL = f"https://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"
TASK_SERVICE_URL = f"https://{TASK_SERVICE_HOST}:{TASK_SERVICE_PORT}"


#Pydantic Models 

#Request and Response Models for API endpoints
def TaskCreate(BaseModel):
    user_id:int
    title: str
    description: Optional[str] = None

def TaskResponse(Basemodel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool

#Health Model - Health Endpoint checks and responses
class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]

class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]




