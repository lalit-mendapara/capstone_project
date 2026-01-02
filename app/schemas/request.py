# Pydantic models ensure the API only accepts the correct data format.
from pydantic import BaseModel

class ChatQuery(BaseModel):
    text: str

class ChatResponse(BaseModel):
    answer: str
    status: str = "success"