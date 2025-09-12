from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user_router

"""from models.db import LocalSession"""
from sqlalchemy.orm import Session

"""from models.db import Base, engine"""

"""Base.metadata.create_all(bind=engine)"""

app = FastAPI()
app.include_router(user_router)


@app.get("/")
async def home():
    return "API connection Successful. Welcome to Orbituwa"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URLs to allow
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE all allowed
    allow_headers=["*"],  # All headers allowed
)
