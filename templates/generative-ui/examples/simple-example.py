"""
Simple Standalone Example

A minimal example showing the core concept of Generative UI with AG2.
This can be run independently without the full frontend/backend setup.

Usage:
    export OPENAI_API_KEY='sk-...'
    python examples/simple-example.py
"""

import os
from autogen import ConversableAgent, LLMConfig


def main():
    """Run a simple generative UI example."""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='sk-...'")
        return
    
    # Configure LLM
    llm_config = LLMConfig({
        "api_type": "openai",
        "model": "gpt-4o-mini",
        "api_key": api_key,
        "temperature": 0.7,
    })
    
    # Create a UI Generator agent
    ui_agent = ConversableAgent(
        name="ui_generator",
        system_message="""You are a UI component generator. 
        When given a request, generate a UI component in JSON format.
        
        Example format:
        ```json
        {
            "type": "card",
            "title": "Welcome",
            "content": "Hello, world!",
            "data": {}
        }
        ```
        
        Available types: card, alert, table
        """,
        llm_config=llm_config,
    )
    
    # Create a user proxy (represents the user)
    user = ConversableAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )
    
    # Example requests
    requests = [
        "Create a welcome card for a new user",
        "Generate an alert about system maintenance",
        "Show a table with sample product data",
    ]
    
    print("=" * 70)
    print(" Simple Generative UI Example with AG2 ")
    print("=" * 70)
    print()
    
    for i, request in enumerate(requests, 1):
        print(f"\n{'─' * 70}")
        print(f"Request {i}: {request}")
        print('─' * 70)
        
        # Generate UI component
        result = user.initiate_chat(
            ui_agent,
            message=request,
            max_turns=1,
        )
        
        # Extract and display the component
        if result.chat_history:
            response = result.chat_history[-1].get("content", "")
            
            # Try to extract JSON
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                component = response[start:end].strip()
                
                print("\nGenerated Component:")
                print(component)
            else:
                print("\nResponse:")
                print(response)
    
    print("\n" + "=" * 70)
    print("\nNext Steps:")
    print("1. Try modifying the requests above")
    print("2. Experiment with different component types")
    print("3. Explore the full template in templates/generative-ui/")
    print("=" * 70)


if __name__ == "__main__":
    main()
