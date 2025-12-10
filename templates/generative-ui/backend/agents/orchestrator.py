"""
AG2 Agent Orchestrator for Generative UI.

This module defines the multi-agent workflow that coordinates
different specialized agents to generate UI components.
"""

import os
from typing import Any, AsyncGenerator, Dict, List

from autogen import ConversableAgent, GroupChat, GroupChatManager, LLMConfig


def create_llm_config() -> LLMConfig:
    """Create LLM configuration from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return LLMConfig({
        "api_type": "openai",
        "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
        "api_key": api_key,
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    })


def create_ui_generator_agent(llm_config: LLMConfig) -> ConversableAgent:
    """
    Create the UI Generator Agent.
    
    This agent specializes in generating UI component definitions
    in a structured JSON format.
    """
    system_message = """You are a UI Generator Agent. Your role is to create 
    structured UI component definitions based on user queries and data.
    
    Always respond with valid JSON in this format:
    {
        "type": "component_type",  // e.g., "card", "chart", "table", "form"
        "title": "Component Title",
        "content": "Main content or description",
        "data": {},  // Any structured data needed for the component
        "actions": []  // Optional: buttons or interactive elements
    }
    
    Available component types:
    - card: Information display
    - chart: Data visualization
    - table: Tabular data
    - form: Input collection
    - list: Ordered or unordered items
    - alert: Important messages
    
    Be creative and contextual in your component choices."""
    
    return ConversableAgent(
        name="ui_generator",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )


def create_data_agent(llm_config: LLMConfig) -> ConversableAgent:
    """
    Create the Data Agent.
    
    This agent handles data fetching, processing, and formatting.
    """
    system_message = """You are a Data Agent. Your role is to:
    1. Understand what data is needed based on user queries
    2. Format data in a structured way for UI components
    3. Provide context and insights about the data
    
    When you receive a query, analyze what data would be most relevant
    and respond with structured information that can be displayed."""
    
    return ConversableAgent(
        name="data_agent",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )


def create_orchestrator_agent(llm_config: LLMConfig) -> ConversableAgent:
    """
    Create the Orchestrator Agent.
    
    This agent coordinates the workflow and decides which agents to involve.
    """
    system_message = """You are the Orchestrator Agent. Your role is to:
    1. Analyze user queries and understand intent
    2. Coordinate with specialized agents (UI Generator, Data Agent)
    3. Ensure responses are coherent and well-structured
    4. Decide when the task is complete
    
    When you receive a query:
    1. Understand what the user wants
    2. Involve the Data Agent if data is needed
    3. Ask the UI Generator to create appropriate components
    4. Respond with "COMPLETE" when done."""
    
    return ConversableAgent(
        name="orchestrator",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "COMPLETE" in (x.get("content", "") or "").upper(),
    )


class AgentWorkflow:
    """Manages the multi-agent workflow for UI generation."""
    
    def __init__(self):
        self.llm_config = create_llm_config()
        self.orchestrator = create_orchestrator_agent(self.llm_config)
        self.ui_generator = create_ui_generator_agent(self.llm_config)
        self.data_agent = create_data_agent(self.llm_config)
        
        # Create group chat
        self.group_chat = GroupChat(
            agents=[self.orchestrator, self.ui_generator, self.data_agent],
            messages=[],
            max_round=10,
            speaker_selection_method="auto",
        )
        
        self.manager = GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.llm_config,
        )
    
    async def run(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent workflow synchronously.
        
        Args:
            query: User query
            context: Additional context
        
        Returns:
            Dictionary with components and metadata
        """
        # Start the conversation
        result = self.orchestrator.initiate_chat(
            self.manager,
            message=query,
            max_turns=10,
        )
        
        # Extract UI components from the conversation
        components = self._extract_components(result.chat_history)
        
        return {
            "components": components,
            "metadata": {
                "messages": len(result.chat_history),
                "cost": result.cost if hasattr(result, "cost") else None,
            }
        }
    
    async def stream(
        self, query: str, context: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream the agent workflow results.
        
        Args:
            query: User query
            context: Additional context
        
        Yields:
            Dictionaries containing agent messages and components
        """
        # For now, simulate streaming with the full result
        # In production, you'd hook into AG2's streaming capabilities
        result = await self.run(query, context)
        
        for component in result["components"]:
            yield {
                "type": "component",
                "component": component,
                "agent": "ui_generator",
            }
    
    def _extract_components(self, chat_history: List[Dict]) -> List[Dict]:
        """Extract UI component definitions from chat history."""
        components = []
        
        for message in chat_history:
            content = message.get("content", "")
            
            # Try to parse JSON components
            if "```json" in content:
                # Extract JSON from markdown code blocks
                import json
                try:
                    start = content.find("```json") + 7
                    end = content.find("```", start)
                    json_str = content[start:end].strip()
                    component = json.loads(json_str)
                    components.append(component)
                except (json.JSONDecodeError, ValueError):
                    pass
            elif content.startswith("{") and content.endswith("}"):
                # Try to parse as JSON
                import json
                try:
                    component = json.loads(content)
                    if "type" in component:
                        components.append(component)
                except (json.JSONDecodeError, ValueError):
                    pass
        
        return components


def create_agent_workflow() -> AgentWorkflow:
    """Create and return a new agent workflow instance."""
    return AgentWorkflow()
