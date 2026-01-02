# Initializes everything and sets up the REST Standards.

from fastapi import FastAPI 
from app.api import chat
from app.core.config import settings
from app.db.session import engine
from app.db import models

# Create Postgres Tables on startup
models.Base.metadata.create_all(bind=engine) # engine=The connection manager for your PostgreSQL database.

app = FastAPI(title=settings.PROJECT_NAME) #app=The main object that represents your entire web server.

# Include the Chat Router
app.include_router(chat.router, prefix="/api/v1") # router=A mini-module containing specific "routes" (paths) for the chat AI.

@app.get("/health")
def health():
    return {"status": "healthy"}