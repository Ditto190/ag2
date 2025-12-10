"""
Example: Data Agent

This agent handles data fetching, processing, and formatting for UI components.
It can connect to various data sources and prepare data for visualization.
"""

import os
import autogen
from typing import Dict, Any, List, Optional


def create_data_fetcher_agent() -> autogen.ConversableAgent:
    """
    Create a data agent that fetches and processes data for UI components.
    
    This agent can:
    1. Connect to various data sources (APIs, databases, files)
    2. Transform and filter data
    3. Format data for specific UI components
    4. Aggregate and compute metrics
    """
    
    system_message = """You are a Data Processing Agent. Your role is to:
    
    1. Fetch data from various sources when requested
    2. Transform and clean data as needed
    3. Format data appropriately for UI components
    4. Calculate metrics and aggregations
    5. Handle data validation and error cases
    
    When working with data:
    - Ensure data types are correct
    - Handle missing or null values
    - Apply appropriate transformations
    - Optimize data structure for the target UI component
    """
    
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY", "your-api-key")
            }
        ],
        "temperature": 0.3,  # Lower temperature for more consistent data handling
    }
    
    agent = autogen.ConversableAgent(
        name="data_processor",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Register data tools
    @agent.register_for_llm(description="Fetch user data from the system")
    def fetch_users(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch user data with optional filters."""
        # Mock data - in production, this would query a real database
        users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
            {"id": 3, "name": "Carol", "email": "carol@example.com", "role": "user"},
        ]
        
        if filters:
            for key, value in filters.items():
                users = [u for u in users if u.get(key) == value]
        
        return users
    
    @agent.register_for_execution()
    def fetch_users(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
            {"id": 3, "name": "Carol", "email": "carol@example.com", "role": "user"},
        ]
        
        if filters:
            for key, value in filters.items():
                users = [u for u in users if u.get(key) == value]
        
        return users
    
    @agent.register_for_llm(description="Calculate metrics from data")
    def calculate_metrics(data: List[Dict[str, Any]], metric_fields: List[str]) -> Dict[str, Any]:
        """Calculate basic metrics from data."""
        metrics = {
            "total_count": len(data)
        }
        
        for field in metric_fields:
            values = [item.get(field) for item in data if item.get(field) is not None]
            if values and all(isinstance(v, (int, float)) for v in values):
                metrics[f"{field}_sum"] = sum(values)
                metrics[f"{field}_avg"] = sum(values) / len(values)
                metrics[f"{field}_min"] = min(values)
                metrics[f"{field}_max"] = max(values)
        
        return metrics
    
    @agent.register_for_execution()
    def calculate_metrics(data: List[Dict[str, Any]], metric_fields: List[str]) -> Dict[str, Any]:
        metrics = {
            "total_count": len(data)
        }
        
        for field in metric_fields:
            values = [item.get(field) for item in data if item.get(field) is not None]
            if values and all(isinstance(v, (int, float)) for v in values):
                metrics[f"{field}_sum"] = sum(values)
                metrics[f"{field}_avg"] = sum(values) / len(values)
                metrics[f"{field}_min"] = min(values)
                metrics[f"{field}_max"] = max(values)
        
        return metrics
    
    @agent.register_for_llm(description="Format data for table display")
    def format_for_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Format data for table UI component."""
        if not data:
            return {"headers": [], "rows": []}
        
        headers = columns or list(data[0].keys())
        rows = [[item.get(col, "") for col in headers] for item in data]
        
        return {
            "headers": headers,
            "rows": rows,
            "total_rows": len(rows)
        }
    
    @agent.register_for_execution()
    def format_for_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> Dict[str, Any]:
        if not data:
            return {"headers": [], "rows": []}
        
        headers = columns or list(data[0].keys())
        rows = [[item.get(col, "") for col in headers] for item in data]
        
        return {
            "headers": headers,
            "rows": rows,
            "total_rows": len(rows)
        }
    
    return agent


# Example usage
if __name__ == "__main__":
    data_agent = create_data_fetcher_agent()
    
    print("Data Agent created!")
    print("This agent can fetch and process data for UI components.")
    
    # Example: The agent could fetch users and format them for a table
    # users = fetch_users()
    # table_data = format_for_table(users, columns=["name", "email", "role"])
