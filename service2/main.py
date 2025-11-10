#service2/main.py
import os
from httpx
import time
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict

#Initialize FastAPI
task_service = FastAPI(title="Task Services", version = "1.0.0")

