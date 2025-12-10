"""
Chat Interface Example

This example demonstrates a conversational interface where agents
generate UI components based on user interactions.

Usage:
    python examples/chat-interface.py
"""

import os
import sys

# Add parent directory to path to import from backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from autogen import ConversableAgent, GroupChat, GroupChatManager, LLMConfig


def create_chat_interface():
    """Create a chat interface with specialized agents."""
    
    # Configure LLM
    llm_config = LLMConfig({
        "api_type": "openai",
        "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.7,
    })
    
    # Intent Analyzer - Understands user intent
    intent_analyzer = ConversableAgent(
        name="intent_analyzer",
        system_message="""You are an Intent Analyzer. Your role is to:
        1. Understand the user's intent from their message
        2. Determine what type of response is needed
        3. Identify if a form, information display, or action is required
        
        Respond with a brief analysis of the user's intent.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # UI Generator - Creates appropriate UI components
    ui_generator = ConversableAgent(
        name="ui_generator",
        system_message="""You are a UI Generator. Based on the user's intent, 
        create appropriate UI components in JSON format.
        
        Available components:
        - card: For displaying information
        - form: For collecting user input (coming soon)
        - alert: For important messages
        - table: For structured data
        
        Example response:
        ```json
        {
            "type": "card",
            "title": "Support Ticket",
            "content": "Please describe your issue...",
            "actions": [
                {"label": "Submit", "action": "submit_ticket"}
            ]
        }
        ```
        
        Always respond with valid JSON.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Coordinator - Manages the conversation flow
    coordinator = ConversableAgent(
        name="coordinator",
        system_message="""You are the Coordinator. You ensure the conversation
        flows smoothly and that appropriate UI components are generated.
        
        When the UI Generator provides a component, say 'COMPLETE'.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "COMPLETE" in (x.get("content", "") or "").upper(),
    )
    
    # Create group chat
    group_chat = GroupChat(
        agents=[coordinator, intent_analyzer, ui_generator],
        messages=[],
        max_round=8,
        speaker_selection_method="auto",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
    )
    
    return coordinator, manager


def run_example():
    """Run the chat interface example."""
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='sk-...'")
        return
    
    print("=" * 60)
    print("Chat Interface Example - AG2 Generative UI")
    print("=" * 60)
    print("\nThis example shows how agents generate UI components")
    print("based on conversational context.\n")
    
    # Create the interface
    coordinator, manager = create_chat_interface()
    
    # Example queries
    examples = [
        "I need to report a bug in the application",
        "Show me my account information",
        "I want to change my password",
    ]
    
    print("Example queries:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    
    print("\n" + "=" * 60)
    
    # Run a sample query
    user_message = examples[0]
    print(f"\nUser: {user_message}\n")
    
    result = coordinator.initiate_chat(
        manager,
        message=user_message,
        max_turns=8,
    )
    
    print("\n" + "=" * 60)
    print("Chat completed!")
    print(f"Total messages: {len(result.chat_history)}")
    
    # Extract and display UI components
    print("\nGenerated UI Components:")
    for msg in result.chat_history:
        content = msg.get("content", "")
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            component_json = content[start:end].strip()
            print(f"\n{component_json}")


if __name__ == "__main__":
    run_example()
