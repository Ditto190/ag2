"""
Data Dashboard Example

This example demonstrates how agents can generate data visualizations
and analytics dashboards based on natural language queries.

Usage:
    python examples/data-dashboard.py
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path to import from backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from autogen import ConversableAgent, GroupChat, GroupChatManager, LLMConfig
from typing import Annotated


def generate_sample_sales_data():
    """Generate sample sales data for demonstration."""
    data = []
    for i in range(10):
        data.append({
            "month": f"2024-{i+1:02d}",
            "revenue": random.randint(50000, 150000),
            "expenses": random.randint(30000, 80000),
            "customers": random.randint(100, 500),
        })
    return data


def create_dashboard_agents():
    """Create specialized agents for dashboard generation."""
    
    llm_config = LLMConfig({
        "api_type": "openai",
        "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.7,
    })
    
    # Data Analyst - Understands data queries and requirements
    data_analyst = ConversableAgent(
        name="data_analyst",
        system_message="""You are a Data Analyst. Your role is to:
        1. Understand what data the user wants to see
        2. Determine the best visualization type
        3. Request data from the Data Provider
        4. Analyze the data and extract insights
        
        Available visualization types:
        - table: For raw data display
        - card: For summary metrics
        - chart: For trends and comparisons (requires implementation)
        """,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Data Provider - Fetches and formats data
    data_provider = ConversableAgent(
        name="data_provider",
        system_message="""You are a Data Provider. When asked for data:
        1. Provide sample data in a structured format
        2. Format data appropriately for visualization
        3. Include relevant metrics and summaries
        
        For sales data, include: month, revenue, expenses, customers
        Format as JSON with clear structure.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Dashboard Builder - Creates dashboard components
    dashboard_builder = ConversableAgent(
        name="dashboard_builder",
        system_message="""You are a Dashboard Builder. Your role is to:
        1. Take data and insights from the analyst
        2. Create appropriate UI components
        3. Structure multiple components into a cohesive dashboard
        
        Create components in JSON format:
        
        For tables:
        ```json
        {
            "type": "table",
            "title": "Sales Data",
            "data": {
                "headers": ["Month", "Revenue", "Expenses", "Profit"],
                "rows": [["2024-01", 100000, 50000, 50000]]
            }
        }
        ```
        
        For summary cards:
        ```json
        {
            "type": "card",
            "title": "Total Revenue",
            "content": "Summary of total revenue across all periods",
            "data": {
                "Total": "$1,200,000",
                "Average": "$100,000",
                "Growth": "+15%"
            }
        }
        ```
        
        You can create multiple components for a comprehensive dashboard.
        Say 'DASHBOARD_COMPLETE' when done.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "DASHBOARD_COMPLETE" in (x.get("content", "") or "").upper(),
    )
    
    # Create group chat
    group_chat = GroupChat(
        agents=[data_analyst, data_provider, dashboard_builder],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
    )
    
    return data_analyst, manager


def run_example():
    """Run the data dashboard example."""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    print("=" * 60)
    print("Data Dashboard Example - AG2 Generative UI")
    print("=" * 60)
    print("\nThis example shows how agents generate data dashboards")
    print("with tables, metrics, and insights.\n")
    
    # Create agents
    analyst, manager = create_dashboard_agents()
    
    # Example query
    query = "Show me sales performance for the year with revenue, expenses, and profit analysis"
    
    print(f"Query: {query}\n")
    print("=" * 60)
    
    # Run the analysis
    result = analyst.initiate_chat(
        manager,
        message=query,
        max_turns=12,
    )
    
    print("\n" + "=" * 60)
    print("Dashboard generation completed!")
    print(f"Total messages: {len(result.chat_history)}")
    
    # Extract components
    print("\nGenerated Dashboard Components:")
    component_count = 0
    for msg in result.chat_history:
        content = msg.get("content", "")
        if "```json" in content:
            component_count += 1
            start = content.find("```json") + 7
            end = content.find("```", start)
            component_json = content[start:end].strip()
            print(f"\nComponent {component_count}:")
            print(component_json)
    
    if component_count == 0:
        print("\nNo components generated in expected format.")
        print("Full conversation available in result.chat_history")


if __name__ == "__main__":
    run_example()
