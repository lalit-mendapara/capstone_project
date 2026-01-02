#Connects the API to the logic and includes Industry Level Error Handling.

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.schemas.request import ChatQuery, ChatResponse
from app.services.ai_logic import get_dynamic_answer
from app.tasks.worker import ingest_faq_file
from app.db.session import get_db
from app.db.models import ChatLog
import logging
import os

router = APIRouter()
logger = logging.getLogger("api")

@router.post("/ask", response_model=ChatResponse)
async def chat_with_bot(query: ChatQuery, db: Session = Depends(get_db)):
    try:
        # 1. Get the dynamic answer from AI/FAQ logic
        answer = get_dynamic_answer(query.text)
        
        # 2. SAVE TO POSTGRES (Persistence Logic)
        new_log = ChatLog(
            question=query.text,
            answer=answer
        )
        db.add(new_log)
        db.commit() # This writes the data to PostgreSQL
        db.refresh(new_log)
        
        return {"answer": answer, "status": "success"}
    
    except Exception as e:
        db.rollback() # Undo database changes if AI logic fails
        logger.error(f"Chat Error: {str(e)}")
        raise HTTPException(status_code=500, detail="The AI is currently unavailable.")

@router.post("/upload-faq")
async def upload_faq(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        ingest_faq_file.delay(file_path)

        return {"message": f"File '{file.filename}' uploaded and indexing started in background."}
    
    except Exception as e:
        logger.error(f"Upload Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload file.")