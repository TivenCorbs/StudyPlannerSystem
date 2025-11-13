import os
import httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field, Session, create_engine, select


#Initialize FastAPI
app = FastAPI(title="Task Services", version = "1.0.0")



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


engine = create_engine("sqlite:///task.db")


#Pydantic Model 


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


class DependencyStatus(BaseModel):
    status: str
    response_time_ms: Optional[int]


class HealthResponse(BaseModel):
    service: str
    status: str
    dependencies: Optional[Dict[str, DependencyStatus]]



#startup the taskservice database
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)




#HealthCheck
@app.get("/health", response_model= HealthResponse)
async def health_check():


   dependencies = {}
   status = "healthy"


   start_time = time.time()




   try:
       r = httpx.get(f"{USER_SERVICE_URL}/health",timeout=3)
       latency = int((time.time()-start_time)*1000)

       if r.status_code==200:
           dependencies["user_service"] = DependencyStatus(status="healthy",response_time_ms=latency)
       else:
           dependencies["user-service"] = DependencyStatus(status="unhealthy")
           

   except Exception:
       dependencies["unhealthy"] = DependencyStatus(status="unhealthy")
     


   return HealthResponse(service = "task-service",status=status,dependencies=dependencies)






