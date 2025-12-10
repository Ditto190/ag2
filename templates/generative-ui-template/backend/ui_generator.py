"""
UI Generator module for creating dynamic UI components.

This module handles the logic for generating UI components based on
agent responses and user intent.
"""

import json
from typing import Any, Dict, List, Optional


class UIGenerator:
    """
    UIGenerator creates dynamic UI components based on user intent and agent responses.
    """
    
    def __init__(self):
        self.component_templates = self._load_component_templates()
    
    def _load_component_templates(self) -> Dict[str, Any]:
        """Load UI component templates."""
        return {
            "form": {
                "type": "form",
                "layout": "vertical",
                "components": []
            },
            "card": {
                "type": "card",
                "layout": "flex",
                "components": []
            },
            "table": {
                "type": "table",
                "headers": [],
                "rows": []
            },
            "chart": {
                "type": "chart",
                "chartType": "line",
                "data": {}
            },
            "dashboard": {
                "type": "dashboard",
                "layout": "grid",
                "widgets": []
            },
            "chat": {
                "type": "chat",
                "messages": [],
                "inputEnabled": True
            }
        }
    
    def generate(
        self,
        intent: str,
        context: Dict[str, Any],
        agents: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate UI components based on user intent.
        
        Args:
            intent: User's intent or request
            context: Additional context for UI generation
            agents: Dictionary of available agents
            
        Returns:
            Dictionary containing UI component specifications
        """
        # For demonstration, we'll use simple intent matching
        # In a real app, agents would analyze the intent more deeply
        
        intent_lower = intent.lower()
        
        if any(word in intent_lower for word in ["form", "input", "submit", "create"]):
            return self._generate_form(intent, context)
        
        elif any(word in intent_lower for word in ["dashboard", "overview", "metrics"]):
            return self._generate_dashboard(intent, context)
        
        elif any(word in intent_lower for word in ["table", "list", "data"]):
            return self._generate_table(intent, context)
        
        elif any(word in intent_lower for word in ["chart", "graph", "visualization"]):
            return self._generate_chart(intent, context)
        
        elif any(word in intent_lower for word in ["chat", "conversation", "talk"]):
            return self._generate_chat(intent, context)
        
        else:
            return self._generate_default(intent, context)
    
    def _generate_form(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a form UI component."""
        return {
            "type": "form",
            "title": "Dynamic Form",
            "description": f"Generated based on: {intent}",
            "fields": [
                {
                    "name": "name",
                    "label": "Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter your name"
                },
                {
                    "name": "email",
                    "label": "Email",
                    "type": "email",
                    "required": True,
                    "placeholder": "your.email@example.com"
                },
                {
                    "name": "message",
                    "label": "Message",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Your message here..."
                }
            ],
            "submitButton": {
                "text": "Submit",
                "style": "primary"
            }
        }
    
    def _generate_dashboard(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a dashboard UI component."""
        return {
            "type": "dashboard",
            "title": "Analytics Dashboard",
            "description": f"Generated based on: {intent}",
            "widgets": [
                {
                    "type": "metric",
                    "title": "Total Users",
                    "value": "1,234",
                    "change": "+12%",
                    "trend": "up"
                },
                {
                    "type": "metric",
                    "title": "Active Sessions",
                    "value": "567",
                    "change": "+5%",
                    "trend": "up"
                },
                {
                    "type": "metric",
                    "title": "Revenue",
                    "value": "$12,500",
                    "change": "+8%",
                    "trend": "up"
                },
                {
                    "type": "chart",
                    "title": "User Growth",
                    "chartType": "line",
                    "data": {
                        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                        "datasets": [
                            {
                                "label": "Users",
                                "data": [100, 150, 200, 300, 450, 600]
                            }
                        ]
                    }
                }
            ]
        }
    
    def _generate_table(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a table UI component."""
        return {
            "type": "table",
            "title": "Data Table",
            "description": f"Generated based on: {intent}",
            "headers": ["ID", "Name", "Email", "Status"],
            "rows": [
                ["1", "Alice Smith", "alice@example.com", "Active"],
                ["2", "Bob Johnson", "bob@example.com", "Active"],
                ["3", "Carol White", "carol@example.com", "Inactive"],
            ],
            "pagination": {
                "currentPage": 1,
                "totalPages": 5,
                "itemsPerPage": 10
            },
            "actions": ["view", "edit", "delete"]
        }
    
    def _generate_chart(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a chart UI component."""
        return {
            "type": "chart",
            "title": "Data Visualization",
            "description": f"Generated based on: {intent}",
            "chartType": "bar",
            "data": {
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "datasets": [
                    {
                        "label": "Revenue",
                        "data": [15000, 25000, 35000, 45000],
                        "backgroundColor": "rgba(54, 162, 235, 0.5)"
                    },
                    {
                        "label": "Expenses",
                        "data": [10000, 15000, 20000, 25000],
                        "backgroundColor": "rgba(255, 99, 132, 0.5)"
                    }
                ]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False
            }
        }
    
    def _generate_chat(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a chat UI component."""
        return {
            "type": "chat",
            "title": "AI Assistant Chat",
            "description": f"Generated based on: {intent}",
            "messages": [
                {
                    "id": 1,
                    "sender": "assistant",
                    "text": "Hello! How can I help you today?",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            ],
            "inputPlaceholder": "Type your message...",
            "features": {
                "typing_indicator": True,
                "file_upload": False,
                "voice_input": False
            }
        }
    
    def _generate_default(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a default UI component when intent is unclear."""
        return {
            "type": "card",
            "title": "Welcome",
            "content": f"I'm ready to generate UI based on your needs. You said: '{intent}'",
            "actions": [
                {
                    "label": "Create Form",
                    "action": "generate",
                    "intent": "create a form"
                },
                {
                    "label": "Show Dashboard",
                    "action": "generate",
                    "intent": "show dashboard"
                },
                {
                    "label": "Display Data",
                    "action": "generate",
                    "intent": "show data table"
                }
            ]
        }
    
    def validate_component(self, component: Dict[str, Any]) -> bool:
        """
        Validate a UI component specification.
        
        Args:
            component: Component specification to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["type"]
        return all(field in component for field in required_fields)
    
    def enhance_with_ai(
        self,
        component: Dict[str, Any],
        agent: Any
    ) -> Dict[str, Any]:
        """
        Use an AI agent to enhance a UI component.
        
        Args:
            component: Base component to enhance
            agent: AG2 agent to use for enhancement
            
        Returns:
            Enhanced component specification
        """
        # This would use the agent to improve the component
        # For now, return the component as-is
        return component
