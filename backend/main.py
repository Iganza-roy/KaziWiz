"""
FastAPI Main Application
Multi-Agent Policy Deliberation System Backend
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Dict, Any
from datetime import datetime
import logging
import json
import socketio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import policy service and routes
from app.services.policy_service import PolicyService
from app.api.v1.policy import router as policy_router

# Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
])

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def subscribe_session(sid, data):
    session_id = data.get('session_id')
    if session_id:
        await sio.enter_room(sid, session_id)
        logger.info(f"Client {sid} subscribed to session {session_id}")
        await sio.emit('subscribed', {'session_id': session_id}, room=sid)
        
        # Send a test event to verify connection
        await sio.emit('test_event', {
            'message': 'Test event from backend',
            'timestamp': str(datetime.now())
        }, room=session_id)
        logger.info(f"📤 Sent test_event to session {session_id}")

@sio.event
async def ping(sid):
    await sio.emit('pong', room=sid)

# Initialize policy service with WebSocket event emitter - now Socket.IO
async def emit_websocket_event(event: str, data: dict, session_id: str = None):
    """Emit Socket.IO event to clients"""
    if session_id:
        await sio.emit(event, data, room=session_id)
    else:
        await sio.emit(event, data)

# Create policy service instance
policy_service_instance = PolicyService(event_emitter=emit_websocket_event)

# Make it available for routes
from app.services import policy_service as ps_module
ps_module.policy_service = policy_service_instance

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Multi-Agent Policy Deliberation API")
    logger.info("📊 Initializing SHAP/LIME explainability engine")
    logger.info("🔧 Policy Service initialized with WebSocket events")
    yield
    # Shutdown
    logger.info("👋 Shutting down API")

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Policy Deliberation API",
    description="Real-time AI agent deliberation with SHAP/LIME explainability",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(policy_router)

# Root endpoint
@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "message": "Multi-Agent Policy Deliberation API",
        "version": "1.0.0",
        "docs": "/docs",
        "websocket": "/ws"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Socket.IO enabled API"
    }

# API Routes
@app.get("/api/v1/agents")
async def list_agents():
    """List all available agent types"""
    agents = [
        {"id": "problem_statement", "name": "Problem Statement Expert", "category": "orchestration"},
        {"id": "economic", "name": "Economic Analyst", "category": "core"},
        {"id": "social", "name": "Social Dynamics Expert", "category": "core"},
        {"id": "geospatial", "name": "Geospatial Analyst", "category": "core"},
        {"id": "income", "name": "Income Distribution Analyst", "category": "core"},
        {"id": "resource", "name": "Resource Management Expert", "category": "core"},
        {"id": "legal", "name": "Legal Adviser", "category": "core"},
    ]
    return {"agents": agents, "total": len(agents)}

@app.get("/api/v1/tools")
async def list_tools():
    """List available tools"""
    return {
        "tools": [
            {"id": "web_search", "name": "Web Search", "provider": "Serper"},
            {"id": "wikipedia", "name": "Wikipedia", "type": "knowledge_base"},
            {"id": "arxiv", "name": "ArXiv Research", "type": "knowledge_base"}
        ]
    }

# Test endpoint to emit events
@app.post("/api/v1/test/emit")
async def test_emit(event_type: str, data: Dict[str, Any]):
    """Test endpoint to emit Socket.IO events"""
    await sio.emit(event_type, data)
    return {"status": "emitted", "event": event_type}

# Mount Socket.IO on the FastAPI app - MUST BE LAST
app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/socket.io')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
