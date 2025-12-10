"""
AG2 Agent definitions for Generative UI application.

This module contains pre-configured agents for different roles in the
Generative UI system: coordinator, UI generator, and data handler.
"""

import os
from typing import Annotated, Any, Dict, List, Optional

import autogen
from autogen import ConversableAgent


def get_llm_config() -> dict:
    """
    Get LLM configuration from environment or config file.
    
    Returns:
        dict: LLM configuration for AG2 agents
    """
    # Try to load from OAI_CONFIG_LIST file
    config_list = None
    
    if os.path.exists("OAI_CONFIG_LIST"):
        try:
            config = autogen.LLMConfig.from_json(path="OAI_CONFIG_LIST")
            config_list = config.config_list
        except Exception as e:
            print(f"Warning: Could not load OAI_CONFIG_LIST: {e}")
    
    # Fallback to environment variable
    if not config_list:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            config_list = [
                {
                    "model": os.getenv("MODEL_NAME", "gpt-4"),
                    "api_key": api_key
                }
            ]
    
    if not config_list:
        raise ValueError(
            "No LLM configuration found. Please set OPENAI_API_KEY environment "
            "variable or create an OAI_CONFIG_LIST file."
        )
    
    return {
        "config_list": config_list,
        "temperature": 0.7,
        "timeout": 120,
    }


def create_coordinator_agent() -> ConversableAgent:
    """
    Create a coordinator agent that orchestrates UI generation.
    
    The coordinator analyzes user intent and determines what UI components
    are needed, delegating to specialized agents as necessary.
    
    Returns:
        ConversableAgent: Configured coordinator agent
    """
    system_message = """You are a UI Coordinator Agent. Your role is to:
    1. Analyze user requests and understand their intent
    2. Determine what UI components are needed
    3. Coordinate with other agents to generate appropriate interfaces
    4. Ensure the generated UI is user-friendly and meets requirements
    
    When a user describes what they need, break it down into:
    - The type of interface (form, dashboard, chat, visualization, etc.)
    - Required data and functionality
    - User interaction patterns
    
    Respond with clear instructions for UI generation in JSON format.
    """
    
    return ConversableAgent(
        name="coordinator",
        system_message=system_message,
        llm_config=get_llm_config(),
        human_input_mode="NEVER",
    )


def create_ui_agent() -> ConversableAgent:
    """
    Create a UI generation agent that creates interface components.
    
    This agent specializes in generating UI component specifications
    based on user needs and design principles.
    
    Returns:
        ConversableAgent: Configured UI agent
    """
    system_message = """You are a UI Generation Agent specialized in creating
    dynamic user interfaces. Your responsibilities:
    
    1. Generate UI component specifications in JSON format
    2. Follow modern UI/UX best practices
    3. Ensure accessibility and responsiveness
    4. Create intuitive and user-friendly interfaces
    
    When generating UI, consider:
    - Component hierarchy and layout
    - User interaction patterns
    - Visual design principles
    - Accessibility requirements
    
    Output UI specifications as structured JSON with:
    - component_type: Type of component (form, card, list, chart, etc.)
    - properties: Component-specific properties
    - children: Nested components if applicable
    - events: User interaction handlers
    """
    
    return ConversableAgent(
        name="ui_generator",
        system_message=system_message,
        llm_config=get_llm_config(),
        human_input_mode="NEVER",
    )


def create_data_agent() -> ConversableAgent:
    """
    Create a data agent that handles data fetching and processing.
    
    This agent can be extended with tools to fetch real data from APIs,
    databases, or other sources to populate the generated UI.
    
    Returns:
        ConversableAgent: Configured data agent
    """
    system_message = """You are a Data Agent responsible for:
    1. Fetching data from various sources when needed
    2. Processing and formatting data for UI display
    3. Handling data validation and transformation
    
    When working with data:
    - Ensure data is in the correct format for the UI
    - Handle errors gracefully
    - Optimize data structure for performance
    - Apply necessary transformations
    """
    
    llm_config = get_llm_config()
    
    agent = ConversableAgent(
        name="data_handler",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Register example tool for data fetching
    @agent.register_for_llm(description="Fetch sample data for UI components")
    def fetch_sample_data(data_type: Annotated[str, "Type of data to fetch"]) -> dict:
        """Fetch sample data based on type."""
        sample_data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ],
            "products": [
                {"id": 1, "name": "Widget", "price": 29.99},
                {"id": 2, "name": "Gadget", "price": 49.99},
            ],
            "metrics": {
                "total_users": 150,
                "active_sessions": 42,
                "revenue": 12500.50,
            }
        }
        
        return sample_data.get(data_type, {})
    
    @agent.register_for_execution()
    def fetch_sample_data(data_type: str) -> dict:
        """Execution implementation."""
        sample_data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ],
            "products": [
                {"id": 1, "name": "Widget", "price": 29.99},
                {"id": 2, "name": "Gadget", "price": 49.99},
            ],
            "metrics": {
                "total_users": 150,
                "active_sessions": 42,
                "revenue": 12500.50,
            }
        }
        
        return sample_data.get(data_type, {})
    
    return agent


def create_chat_agent() -> ConversableAgent:
    """
    Create a conversational agent for chat-based UI interactions.
    
    This agent handles natural language conversations and can trigger
    UI updates based on the conversation context.
    
    Returns:
        ConversableAgent: Configured chat agent
    """
    system_message = """You are a friendly and helpful Chat Agent. Your role:
    1. Engage in natural conversations with users
    2. Understand user needs and preferences
    3. Suggest UI components or actions based on conversation
    4. Provide helpful information and guidance
    
    Be conversational, friendly, and clear in your responses.
    When appropriate, suggest UI changes or actions that would help the user.
    """
    
    return ConversableAgent(
        name="chat_assistant",
        system_message=system_message,
        llm_config=get_llm_config(),
        human_input_mode="NEVER",
    )


# Example: Creating a multi-agent workflow
def create_ui_generation_workflow() -> Dict[str, ConversableAgent]:
    """
    Create a complete workflow with multiple agents for UI generation.
    
    Returns:
        dict: Dictionary of agents for the workflow
    """
    return {
        "coordinator": create_coordinator_agent(),
        "ui_generator": create_ui_agent(),
        "data_handler": create_data_agent(),
        "chat_assistant": create_chat_agent(),
    }
