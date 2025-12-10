"""
Example: Chat Agent for Generative UI

This example shows how to create a conversational agent that can
dynamically generate UI components based on natural language conversation.
"""

import os
import autogen
from typing import Dict, Any


def create_chat_ui_agent() -> autogen.ConversableAgent:
    """
    Create a chat agent that generates UI through conversation.
    
    This agent can:
    1. Understand user needs through natural language
    2. Suggest appropriate UI components
    3. Generate UI specifications on demand
    """
    
    system_message = """You are a helpful UI assistant that helps users 
    create interfaces through conversation. 
    
    When a user describes what they need:
    1. Ask clarifying questions if needed
    2. Suggest appropriate UI components (forms, tables, dashboards, etc.)
    3. Generate detailed UI specifications in JSON format
    
    Always be friendly and helpful. Make sure the UI you suggest matches
    the user's actual needs.
    """
    
    # Use the shared get_llm_config function from backend.agents
    # In production, import: from backend.agents import get_llm_config
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY", "your-api-key")
            }
        ],
        "temperature": 0.7,
    }
    
    return autogen.ConversableAgent(
        name="chat_ui_assistant",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )


# Example usage
if __name__ == "__main__":
    agent = create_chat_ui_agent()
    
    # Example interaction
    user_request = "I need a way for users to contact us"
    
    # In a real app, you'd initiate a chat with the agent
    print(f"User: {user_request}")
    print("Agent would analyze this and generate a contact form UI")
