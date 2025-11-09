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

pip install sqlmodel

Usage Instructions: 


API Documentation: 

https://sqlmodel.tiangolo.com/ 

Testing:

Project Structure:
