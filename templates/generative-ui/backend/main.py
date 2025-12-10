import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import create_agent_workflow
from schemas.messages import GenerateRequest, GenerateResponse, StreamChunk


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for FastAPI app."""
    print("🚀 Starting AG2 Generative UI Backend...")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="AG2 Generative UI API",
    description="Backend API for Generative UI applications powered by AG2",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ag2-generative-ui"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_ui(request: GenerateRequest) -> GenerateResponse:
    """
    Generate UI components based on user query.
    
    This endpoint orchestrates AG2 agents to process the query
    and return structured UI component definitions.
    """
    try:
        workflow = create_agent_workflow()
        result = await workflow.run(request.query, request.context)
        
        return GenerateResponse(
            components=result.get("components", []),
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        return GenerateResponse(
            components=[],
            metadata={"error": str(e)},
        )


@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    """
    WebSocket endpoint for streaming UI generation.
    
    Provides real-time streaming of agent thoughts and UI components
    as they are generated.
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            query = data.get("query", "")
            context = data.get("context", {})
            
            if not query:
                await websocket.send_json({
                    "type": "error",
                    "message": "Query is required"
                })
                continue
            
            # Create workflow and stream results
            workflow = create_agent_workflow()
            
            try:
                async for chunk in workflow.stream(query, context):
                    await websocket.send_json({
                        "type": chunk.get("type", "stream"),
                        "content": chunk.get("content"),
                        "component": chunk.get("component"),
                        "agent": chunk.get("agent"),
                    })
                
                # Send completion signal
                await websocket.send_json({
                    "type": "complete",
                    "message": "Generation complete"
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.post("/api/chat")
async def chat(request: BaseModel):
    """
    Simple chat endpoint for conversational interactions.
    
    Note: This is a placeholder endpoint. In production, implement:
    1. Message history management
    2. Agent conversation handling
    3. Proper response formatting
    
    See the /api/generate endpoint for a working example.
    """
    return {
        "message": "Chat endpoint - implement your logic here",
        "note": "This is a placeholder. See /docs for API documentation."
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )
