

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import time
import redis
import os
from sqlmodel import SQLModel, Field, session, create_engine, select


#Intiliazing FASTAPI
app = FastAPI()




#Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./user.db")
engine = create_engine(DATABASE_URL, echo=True)




#Redis Config
REDIS_HOST = os.getenv("REDISHOST",redis)
REDIS_PORT = int(os.getenv("REDIS_PORT",6379))


#Trying Redis Connection
try:
   redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except Exception as e:
   print(f"Redis connection failed: {e}")
   redis_client = None




#Pydantic Models for SQLMODEL


class User_Table(SQLModel, table=True):
   __tablename__ = "users"
   id: Optional[int] = Field(default=None, primary_key=True)
   name: str = Field(index=True)
   email: EmailStr = Field(unique=True, index=True)
   password: str




class UserCreate(BaseModel):
   name: str
   email: str
   password:str


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








@app.get("/")
def root():
   return {"Message": "USER_SERVICE SQLMODEL is Runnning"}




#Creating  ENDPOINT (POST/USERS)
#This will allow clients (or other services) to create a user
#Pydantic will then verify to see if it is valid
@app.post("/users", response_model = UserResponse)
async def create_user(user: UserCreate):


 with session(engine) as session:
  
   existing_user = session.exec(select(User_Table).where(User_Table.email == user.email)).first()
   if existing_user:
       raise HTTPException(status_code=400,detail= "Email Already Exists")




   new_user = User_Table(name=user.name, email = user.email, password = user.password)
   session.add(new_user)
   session.commit()
   session.refresh(new_user)
   return new_user






#Get all users from database
@app.get("/users", response_model=list[UserResponse])
def get_all_users():
   with session(engine) as session:
       users = session.exec(select(User_Table)).all()
       return users


#Maybe add later
#@app.delete("/users/{user_id}", status_code= status.HTTP_204_NO_CONTEXT)




#HealthCheck


#Health Endpoint


@app.get("/health")
async def health_check():


   dependencies = {}
   status = "healthy"


   start_time = time.time()




   try:
       redis_client.ping()
       latency = round((time.time() - start_time)*1000)
       dependencies["healthy"] = DependencyStatus(status="healthy",response_time_ms=latency)


   except Exception:
       dependencies["unhealthy"] = DependencyStatus(status="unhealthy")
       status = "unhealthy"


   return HealthResponse(service = "user-service",status=status,dependencies=dependencies)





