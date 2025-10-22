"""
Policy Service - WebSocket-enabled policy deliberation with Real AI Agents
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
import json
import logging

from .integrated_deliberation import IntegratedDeliberationSystem

logger = logging.getLogger(__name__)


@dataclass
class PolicySession:
    """Represents a policy deliberation session"""
    session_id: str
    policy_topic: str
    background_context: str
    status: str  # 'initializing', 'running', 'completed', 'error'
    current_phase: int
    phase_name: str
    created_at: str
    updated_at: str
    agents_status: Dict[str, Any]
    results: Dict[str, Any]


class PolicyService:
    """
    Service layer for policy deliberation with Real AI Agents
    """
    
    def __init__(self, event_emitter: Optional[Callable] = None):
        """
        Initialize policy service
        
        Args:
            event_emitter: Async function to emit WebSocket events
        """
        self.event_emitter = event_emitter
        self.active_sessions: Dict[str, PolicySession] = {}
        self.deliberation_system = IntegratedDeliberationSystem(event_emitter=event_emitter)
        logger.info("✅ Policy Service initialized with Real Agent System")
        
    async def emit_event(self, event: str, data: dict, session_id: str = None):
        """Emit WebSocket event if emitter is available"""
        if self.event_emitter:
            try:
                await self.event_emitter(event, data, session_id)
            except Exception as e:
                print(f"Error emitting event {event}: {e}")
    
    async def create_session(self, policy_data: dict) -> PolicySession:
        """
        Create a new policy deliberation session
        
        Args:
            policy_data: Dict with policy_topic, background_context, etc.
            
        Returns:
            PolicySession object
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        session = PolicySession(
            session_id=session_id,
            policy_topic=policy_data.get('policy_topic', ''),
            background_context=policy_data.get('background_context', ''),
            status='initializing',
            current_phase=0,
            phase_name='Initialization',
            created_at=now,
            updated_at=now,
            agents_status={},
            results={}
        )
        
        self.active_sessions[session_id] = session
        
        # Emit session created event
        await self.emit_event('session_created', {
            'session_id': session_id,
            'policy_topic': session.policy_topic,
            'created_at': now
        }, session_id)
        
        return session
    
    async def start_deliberation(self, session_id: str):
        """
        Start the deliberation process for a session
        
        Args:
            session_id: Session identifier
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.status = 'running'
        session.updated_at = datetime.utcnow().isoformat()
        
        # Emit deliberation started
        await self.emit_event('deliberation_started', {
            'session_id': session_id,
            'policy_topic': session.policy_topic
        }, session_id)
        
        # Start async deliberation (placeholder - will integrate with agents)
        # This will be replaced with actual agent system integration
        asyncio.create_task(self._run_deliberation(session_id))
    
    async def _run_deliberation(self, session_id: str):
        """
        Run the actual deliberation process with Real AI Agents
        """
        session = self.active_sessions[session_id]
        
        try:
            # Execute real agent deliberation
            result = await self.deliberation_system.run_deliberation(
                session_id=session_id,
                policy_topic=session.policy_topic,
                background_context=session.background_context
            )
            
            if result.get('success'):
                session.status = 'completed'
                session.results = result.get('results', {})
            else:
                session.status = 'error'
                session.results = {'error': result.get('error', 'Unknown error')}
                
        except Exception as e:
            logger.error(f"Deliberation error for session {session_id}: {e}", exc_info=True)
            session.status = 'error'
            session.results = {'error': str(e)}
            await self.emit_event('deliberation_error', {
                'session_id': session_id,
                'error': str(e)
            }, session_id)
        
        session.updated_at = datetime.utcnow().isoformat()
    
    async def _run_phase(self, session_id: str, phase_num: int, phase_name: str, duration: int):
        """Simulate running a phase"""
        session = self.active_sessions[session_id]
        session.current_phase = phase_num
        session.phase_name = phase_name
        session.updated_at = datetime.utcnow().isoformat()
        
        await self.emit_event('phase_changed', {
            'session_id': session_id,
            'phase': phase_num,
            'phase_name': phase_name
        }, session_id)
        
        # Simulate phase work
        await asyncio.sleep(duration)
    
    def get_session(self, session_id: str) -> Optional[PolicySession]:
        """Get session by ID"""
        return self.active_sessions.get(session_id)
    
    def list_sessions(self) -> List[PolicySession]:
        """List all sessions"""
        return list(self.active_sessions.values())
    
    async def update_agent_status(self, session_id: str, agent_name: str, status: dict):
        """Update individual agent status"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.agents_status[agent_name] = status
            session.updated_at = datetime.utcnow().isoformat()
            
            await self.emit_event('agent_status_update', {
                'session_id': session_id,
                'agent_name': agent_name,
                'status': status
            }, session_id)
