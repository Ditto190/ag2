"""Utility functions for the AG2 Generative UI backend."""

import json
from typing import Any, Dict, List, Optional


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from text that might contain markdown code blocks.
    
    Args:
        text: Text potentially containing JSON
    
    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    # Try to find JSON in markdown code blocks
    if "```json" in text:
        try:
            start = text.find("```json") + 7
            end = text.find("```", start)
            json_str = text[start:end].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
    
    # Try to parse the whole text as JSON
    if text.strip().startswith("{"):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
    
    return None


def validate_component(component: Dict[str, Any]) -> bool:
    """
    Validate that a component has the required structure.
    
    Args:
        component: Component dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    return isinstance(component, dict) and "type" in component


def sanitize_component(component: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize component data to ensure it's safe for rendering.
    
    Args:
        component: Component to sanitize
    
    Returns:
        Sanitized component
    """
    # Remove any potentially dangerous fields
    dangerous_fields = ["__proto__", "constructor", "prototype"]
    
    sanitized = {}
    for key, value in component.items():
        if key not in dangerous_fields:
            if isinstance(value, dict):
                sanitized[key] = sanitize_component(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    sanitize_component(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
    
    return sanitized
