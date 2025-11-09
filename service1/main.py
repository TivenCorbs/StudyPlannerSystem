from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import time
import redis
import os 

#Intiliazing FASTAPI
app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("Redis Port", 6379))


class userCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]


#Health Model - Health Endpoint checks and responses
class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]