"""
Policy API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/v1/policy", tags=["policy"])

class PolicyCreate(BaseModel):
    """Policy creation request"""
    policy_topic: str
    background_context: str
    city_data: Optional[str] = ""
    policy_type: Optional[str] = ""
    time_range: Optional[str] = ""
    interests: Optional[str] = ""

class PolicyResponse(BaseModel):
    """Policy session response"""
    session_id: str
    policy_topic: str
    background_context: str
    status: str
    current_phase: int
    phase_name: str
    created_at: str
    updated_at: str

@router.post("/create", response_model=PolicyResponse)
async def create_policy(policy: PolicyCreate):
    """
    Create a new policy deliberation session
    
    This endpoint creates a new session and returns the session ID
    which can be used to subscribe to WebSocket updates
    """
    from app.services import policy_service as ps_module
    
    session = await ps_module.policy_service.create_session({
        'policy_topic': policy.policy_topic,
        'background_context': policy.background_context,
        'city_data': policy.city_data,
        'policy_type': policy.policy_type,
        'time_range': policy.time_range,
        'interests': policy.interests
    })
    
    return PolicyResponse(
        session_id=session.session_id,
        policy_topic=session.policy_topic,
        background_context=session.background_context,
        status=session.status,
        current_phase=session.current_phase,
        phase_name=session.phase_name,
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.post("/start/{session_id}")
async def start_deliberation(session_id: str):
    """
    Start the deliberation process for a session
    """
    from app.services import policy_service as ps_module
    
    session = ps_module.policy_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await ps_module.policy_service.start_deliberation(session_id)
    
    return {"message": "Deliberation started", "session_id": session_id}

@router.get("/session/{session_id}", response_model=PolicyResponse)
async def get_session(session_id: str):
    """
    Get session details
    """
    from app.services import policy_service as ps_module
    
    session = ps_module.policy_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return PolicyResponse(
        session_id=session.session_id,
        policy_topic=session.policy_topic,
        background_context=session.background_context,
        status=session.status,
        current_phase=session.current_phase,
        phase_name=session.phase_name,
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.get("/sessions", response_model=List[PolicyResponse])
async def list_sessions():
    """
    List all policy sessions
    """
    from app.services import policy_service as ps_module
    
    sessions = ps_module.policy_service.list_sessions()
    
    return [
        PolicyResponse(
            session_id=s.session_id,
            policy_topic=s.policy_topic,
            background_context=s.background_context,
            status=s.status,
            current_phase=s.current_phase,
            phase_name=s.phase_name,
            created_at=s.created_at,
            updated_at=s.updated_at
        )
        for s in sessions
    ]
