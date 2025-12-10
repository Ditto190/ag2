"""
Custom tools for AG2 agents in the Generative UI application.

This module provides reusable tools that agents can use to perform
various tasks like data fetching, UI manipulation, and more.
"""

from typing import Annotated, Any, Dict, List, Optional
import json


def create_ui_component(
    component_type: Annotated[str, "Type of UI component to create (form, card, table, etc.)"],
    properties: Annotated[Dict[str, Any], "Properties and configuration for the component"]
) -> Dict[str, Any]:
    """
    Create a UI component specification.
    
    Args:
        component_type: Type of component (form, card, table, chart, etc.)
        properties: Component properties and configuration
        
    Returns:
        UI component specification as a dictionary
    """
    return {
        "type": component_type,
        **properties
    }


def fetch_data(
    source: Annotated[str, "Data source identifier"],
    filters: Annotated[Optional[Dict[str, Any]], "Optional filters to apply"] = None
) -> Dict[str, Any]:
    """
    Fetch data from a specified source.
    
    Args:
        source: Identifier for the data source
        filters: Optional filters to apply to the data
        
    Returns:
        Fetched data as a dictionary
    """
    # This is a mock implementation. In a real app, this would
    # connect to actual data sources (databases, APIs, etc.)
    
    mock_data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
            {"id": 3, "name": "Carol", "email": "carol@example.com", "role": "user"},
        ],
        "products": [
            {"id": 1, "name": "Widget", "price": 29.99, "stock": 100},
            {"id": 2, "name": "Gadget", "price": 49.99, "stock": 50},
            {"id": 3, "name": "Doohickey", "price": 19.99, "stock": 200},
        ],
        "analytics": {
            "total_users": 1234,
            "active_sessions": 567,
            "revenue": 12500.50,
            "growth_rate": 0.15
        }
    }
    
    data = mock_data.get(source, {})
    
    # Apply filters if provided
    if filters and isinstance(data, list):
        for key, value in filters.items():
            data = [item for item in data if item.get(key) == value]
    
    return {"source": source, "data": data}


def validate_form_data(
    form_data: Annotated[Dict[str, Any], "Form data to validate"],
    rules: Annotated[Dict[str, Any], "Validation rules"]
) -> Dict[str, Any]:
    """
    Validate form data against specified rules.
    
    Args:
        form_data: The form data to validate
        rules: Validation rules to apply
        
    Returns:
        Validation result with any errors
    """
    errors = {}
    
    for field, rule in rules.items():
        value = form_data.get(field)
        
        # Check required fields
        if rule.get("required") and not value:
            errors[field] = f"{field} is required"
            continue
        
        # Check type
        if "type" in rule and value is not None:
            expected_type = rule["type"]
            if expected_type == "email" and "@" not in str(value):
                errors[field] = f"{field} must be a valid email"
            elif expected_type == "number":
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors[field] = f"{field} must be a number"
        
        # Check min/max length
        if "minLength" in rule and len(str(value)) < rule["minLength"]:
            errors[field] = f"{field} must be at least {rule['minLength']} characters"
        
        if "maxLength" in rule and len(str(value)) > rule["maxLength"]:
            errors[field] = f"{field} must be at most {rule['maxLength']} characters"
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def format_data_for_display(
    data: Annotated[Any, "Data to format"],
    format_type: Annotated[str, "Desired format (table, list, cards, etc.)"]
) -> Dict[str, Any]:
    """
    Format data for display in UI components.
    
    Args:
        data: Data to format
        format_type: Desired display format
        
    Returns:
        Formatted data structure
    """
    if format_type == "table":
        if isinstance(data, list) and len(data) > 0:
            headers = list(data[0].keys())
            rows = [[item.get(key, "") for key in headers] for item in data]
            return {"headers": headers, "rows": rows}
    
    elif format_type == "cards":
        if isinstance(data, list):
            return {"cards": [{"content": item} for item in data]}
    
    elif format_type == "list":
        if isinstance(data, list):
            return {"items": data}
    
    return {"formatted_data": data}


def calculate_metrics(
    data: Annotated[List[Dict[str, Any]], "Data to analyze"],
    metric_type: Annotated[str, "Type of metric to calculate"]
) -> Dict[str, Any]:
    """
    Calculate metrics from data.
    
    Args:
        data: List of data items
        metric_type: Type of metric (count, sum, average, etc.)
        
    Returns:
        Calculated metrics
    """
    if not data or not isinstance(data, list):
        return {"error": "Invalid data for metrics calculation"}
    
    if metric_type == "count":
        return {"count": len(data)}
    
    elif metric_type == "summary":
        return {
            "total_items": len(data),
            "fields": list(data[0].keys()) if data else [],
            "sample": data[0] if data else None
        }
    
    return {"metric_type": metric_type, "value": len(data)}


def transform_ui_layout(
    components: Annotated[List[Dict[str, Any]], "UI components to arrange"],
    layout_type: Annotated[str, "Layout type (grid, flex, stack, etc.)"]
) -> Dict[str, Any]:
    """
    Transform UI components into a specific layout.
    
    Args:
        components: List of UI components
        layout_type: Desired layout type
        
    Returns:
        Layout specification with arranged components
    """
    layout_configs = {
        "grid": {
            "type": "grid",
            "columns": 3,
            "gap": "1rem"
        },
        "flex": {
            "type": "flex",
            "direction": "row",
            "justify": "space-between"
        },
        "stack": {
            "type": "stack",
            "direction": "vertical",
            "spacing": "1rem"
        }
    }
    
    layout = layout_configs.get(layout_type, layout_configs["stack"])
    layout["components"] = components
    
    return layout


def generate_color_scheme(
    base_color: Annotated[str, "Base color in hex format"],
    scheme_type: Annotated[str, "Type of color scheme (monochromatic, complementary, etc.)"]
) -> Dict[str, List[str]]:
    """
    Generate a color scheme for UI theming.
    
    Args:
        base_color: Base color in hex format (e.g., "#3B82F6")
        scheme_type: Type of color scheme
        
    Returns:
        Dictionary containing color palette
    """
    # This is a simplified implementation
    # In a real app, you'd use proper color theory algorithms
    
    return {
        "primary": base_color,
        "secondary": "#10B981",
        "accent": "#F59E0B",
        "background": "#FFFFFF",
        "text": "#1F2937",
        "scheme_type": scheme_type
    }


# Tool registry for easy access
TOOL_REGISTRY = {
    "create_ui_component": create_ui_component,
    "fetch_data": fetch_data,
    "validate_form_data": validate_form_data,
    "format_data_for_display": format_data_for_display,
    "calculate_metrics": calculate_metrics,
    "transform_ui_layout": transform_ui_layout,
    "generate_color_scheme": generate_color_scheme,
}


def register_tools_with_agent(agent: Any) -> None:
    """
    Register all tools with an AG2 agent.
    
    Args:
        agent: The AG2 agent to register tools with
    """
    for tool_name, tool_func in TOOL_REGISTRY.items():
        agent.register_for_llm(description=tool_func.__doc__)(tool_func)
        agent.register_for_execution()(tool_func)
