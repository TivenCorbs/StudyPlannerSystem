
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


#Trying Redis Connection
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=redis_port, decode_responses=True)
except Exception as e:
    print(f"Redis connection failed: {e}")
    redis_client = None


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

#In memory user store
users_db={}

@app.get("/")
def root():
    return {"Message": "User Service is Running"}


#Creating  ENDPOINT (POST/USERS)
#This will allow clients (or other services) to create a user
#Pydantic will then verify to see if it is valid 
@app.post("/users", response_model = UserResponse)
async def create_user(user: userCreate):

    if user.email in users_db():
        raise HTTPException(status_code=404, detail= "Email Already Exists")
    
    #Increments ID
    user_id = len(users_db)+1
    users_db[user.email] = {"id":user_id,"name":user.name,"email":user.email}

    return users_db[user.email]

#HealthCheck

#Health Endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


