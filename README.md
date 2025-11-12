# StudyPlannerSystem


Study Planner System

Purpose: A microservices-based applications designed in helping students organize and manage their study schedules via tasks, deadlines, and reminders

The system demonstrates a clear service seperation, inter-service communication, and also health monitoring via FastAPI and Docker 

System Purpose

User Service: Manages student accounts
Task Service: tracking studying tasks and deadlines
Reminder Service: gives alerts or notifications about upcoming tasks

Each of the systems will have to be independent from each other's contaienrs which will allow scalability and modularity. Also they would use health check endpoints to help make sure they are reliable across the services


Prerequisites: Required Software
Python 3.11 
Docker Compose
Docker
Docker Desktop 

Installation & setup

pip install fastapi uvicorn httpx pydantic

pip list

pip install sqlmodel

You should see
fastapi
httpx
pydantic
uvicorn

Run the App Using: 
uvicorn main:app --reload



Usage Instructions: 


API Documentation: 

https://sqlmodel.tiangolo.com/ 

https://docs.pydantic.dev/latest/#pydantic-examples 

https://fastapi.tiangolo.com/#create-it 

https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

Testing:

Docker Commands (Friendly Reminder)

Run the container
docker run -d -p 8000:8000 fastapi-app

Container ID
docker ps

Stop By Name or ID

docker stop <container_id>

Remove Container

docker rm <container_id>

Remove Image

docker rmi fastapi-app

Rebuild and Retest quickly

docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app

Testing Endpoints

curl http://localhost:8000





Project Structure:
