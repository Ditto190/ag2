"""
Main FastAPI application for Generative UI with AG2 agents.

This application demonstrates how to build a Generative UI system where
AI agents dynamically create and modify user interface components based on
user interactions and application state.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agents import create_ui_agent, create_data_agent, create_coordinator_agent
from ui_generator import UIGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Generative UI with AG2",
    description="A template for building Generative UI applications with agentic AI",
    version="1.0.0"
)

# Setup paths
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize UI generator
ui_generator = UIGenerator()

# Store active WebSocket connections
active_connections: List[WebSocket] = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main application page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Generative UI with AG2"}
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Generative UI service is running"}


@app.post("/api/generate-ui")
async def generate_ui(request: dict):
    """
    Generate UI components based on user intent.
    
    Args:
        request: Dictionary containing user intent and context
        
    Returns:
        Generated UI components as JSON
    """
    user_intent = request.get("intent", "")
    context = request.get("context", {})
    
    # Create agents
    coordinator = create_coordinator_agent()
    ui_agent = create_ui_agent()
    data_agent = create_data_agent()
    
    # Generate UI based on intent
    ui_components = ui_generator.generate(
        intent=user_intent,
        context=context,
        agents={
            "coordinator": coordinator,
            "ui_agent": ui_agent,
            "data_agent": data_agent
        }
    )
    
    return JSONResponse(content=ui_components)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent communication.
    
    This allows for streaming UI updates as agents process requests.
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            payload = data.get("payload", {})
            
            if message_type == "generate_ui":
                # Stream UI generation updates
                intent = payload.get("intent", "")
                
                # Create agents
                coordinator = create_coordinator_agent()
                ui_agent = create_ui_agent()
                
                # Send initial acknowledgment
                await websocket.send_json({
                    "type": "status",
                    "message": "Processing your request..."
                })
                
                # Generate UI (in a real app, this would stream updates)
                ui_components = ui_generator.generate(
                    intent=intent,
                    context=payload.get("context", {}),
                    agents={
                        "coordinator": coordinator,
                        "ui_agent": ui_agent
                    }
                )
                
                # Send generated UI
                await websocket.send_json({
                    "type": "ui_update",
                    "components": ui_components
                })
                
            elif message_type == "chat":
                # Handle chat messages
                message = payload.get("message", "")
                
                # Echo for now (replace with actual agent logic)
                await websocket.send_json({
                    "type": "chat_response",
                    "message": f"Agent received: {message}"
                })
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    print("🚀 Starting Generative UI application...")
    print(f"📁 Static files: {STATIC_DIR}")
    print(f"📄 Templates: {TEMPLATES_DIR}")
    print("✅ Application ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    print("👋 Shutting down Generative UI application...")


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   Generative UI with AG2                  ║
    ║   🤖 Agentic AI + Dynamic UI              ║
    ╚════════════════════════════════════════════╝
    
    🌐 Server: http://{host}:{port}
    📖 Docs: http://{host}:{port}/docs
    
    Ready to build amazing Generative UI apps!
    """)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
