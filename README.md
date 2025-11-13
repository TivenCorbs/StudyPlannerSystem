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

---
config:
  theme: neo-dark
  look: neo
  layout: elk
---
flowchart TD
    %% app_network - FastAPI Microservices that handles application logic and database
    subgraph app_network["App Network (Docker Compose)"]
        %% User Service (user-service) is built using FastAPI and SQLModel, backed by SQLite.
        %% Handles user authentication (create, authenticate, update), and exposes REST endpoints to other services for validation.
        A["User Service<br/>FastAPI + SQLModel<br/>→ user.db"]
        %% Task Service: uses FastAPI and SQLModel, manages user tasks (to-do, projects, etc).
        %% When a task is created or updated, it validates user id by calling the user service API.
        B["Task Service<br/>FastAPI + SQLModel<br/>→ task.db"]
        %% Scheduler Service handles periodic jobs, reminders, etc.
        %% Reads from scheduler.db; queries user service (for info) and task service (for pending/overdue tasks).
        %% Sends healthchecks to confirm that user and task services are responsive and healthy,
        %% and uses Redis to cache status and health info.
        C["Scheduler Service<br/>FastAPI + SQLModel<br/>→ scheduler.db"]
    end

    %% redis_network - for caching and doing health monitoring via Redis
    subgraph redis_network["Redis Network"]
        %% Redis cache: will store data such as recent service health checks, task/job service info, etc.
        %% (Still considering additional use cases for Redis cache.)
        R[("Redis Cache<br/>(Port 6379)<br/>Dependency health monitoring")]
    end

    %% The Docker Compose environment connects both application and redis networks
    subgraph compose_env["Docker Compose Environment"]
        app_network
        redis_network
    end

    %% User / API Client interacts with the services
    U["User / API Client"] -->|HTTP Requests| A
    U -->|Task operations| B
    U -->|View schedule| C

    %% Task Service validates user using User Service API
    B -->|Validates user via API| A

    %% Scheduler interacts with user and task service for health and task information
    C -->|Checks health & tasks| A & B

    %% Scheduler uses Redis for health/status caching
    C -->|Health pings & caching| R