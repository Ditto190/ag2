"""Pydantic schemas for API requests and responses."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request model for UI generation."""
    
    query: str = Field(..., description="User query or instruction")
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the agents"
    )
    stream: bool = Field(default=False, description="Whether to stream the response")


class UIComponent(BaseModel):
    """Model for a UI component."""
    
    type: str = Field(..., description="Component type (card, chart, table, etc.)")
    title: Optional[str] = Field(None, description="Component title")
    content: Optional[str] = Field(None, description="Main content")
    data: Dict[str, Any] = Field(default_factory=dict, description="Component data")
    actions: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Interactive actions"
    )


class GenerateResponse(BaseModel):
    """Response model for UI generation."""
    
    components: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Generated UI components"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the generation"
    )


class StreamChunk(BaseModel):
    """Model for streaming chunks."""
    
    type: str = Field(..., description="Chunk type (component, stream, error, complete)")
    content: Optional[str] = Field(None, description="Text content")
    component: Optional[Dict[str, Any]] = Field(None, description="Component definition")
    agent: Optional[str] = Field(None, description="Agent that produced this chunk")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ChatMessage(BaseModel):
    """Model for chat messages."""
    
    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    name: Optional[str] = Field(None, description="Agent name")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    message: ChatMessage = Field(..., description="Assistant's response")
    components: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Any UI components to render"
    )
