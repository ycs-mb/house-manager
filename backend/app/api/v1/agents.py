from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

# Lazy initialization of manager agent
_manager = None

def get_manager():
    global _manager
    if _manager is None:
        try:
            from app.agents.manager_agent import ManagerAgent
            _manager = ManagerAgent()
        except Exception as e:
            # If agent initialization fails, return None
            # This allows the API to still work without agent functionality
            print(f"Warning: Could not initialize ManagerAgent: {e}")
            _manager = None
    return _manager

class AgentRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}

@router.post("/request")
async def submit_request(request: AgentRequest, db: Session = Depends(get_db)):
    """
    Submit a prompt to the ManagerAgent for processing
    """
    try:
        manager = get_manager()
        if manager is None:
            return {
                "status": "unavailable",
                "message": "Agent functionality is not configured. Please set OPENAI_API_KEY or other LLM credentials."
            }
        # For Phase 1, we just return a mock response
        # In reality, this would trigger the LangGraph workflow
        result = await manager.process_request(request.prompt)
        return {"status": "processing", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """
    Get the status of a specific agent task
    """
    return {"task_id": task_id, "status": "completed"}
