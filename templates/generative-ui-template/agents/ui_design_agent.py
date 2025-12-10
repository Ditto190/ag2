"""
Example: UI Design Agent

This agent specializes in creating well-designed, accessible UI components
following modern design principles.
"""

import os
import autogen
from typing import Dict, Any, List


def create_ui_design_agent() -> autogen.ConversableAgent:
    """
    Create a UI design agent that focuses on aesthetics and usability.
    
    This agent considers:
    - Visual hierarchy
    - Color theory
    - Typography
    - Spacing and layout
    - Accessibility (WCAG guidelines)
    - Responsive design
    """
    
    system_message = """You are a UI/UX Design Expert Agent. Your role is to
    create beautiful, functional, and accessible user interfaces.
    
    When designing UI components:
    1. Follow modern design principles (spacing, typography, hierarchy)
    2. Ensure accessibility (WCAG 2.1 AA compliance)
    3. Consider responsive design for all screen sizes
    4. Use appropriate color schemes and contrast
    5. Create intuitive user interactions
    
    Output UI specifications with:
    - Component structure (HTML-like)
    - Styling information (colors, spacing, typography)
    - Interaction patterns
    - Accessibility attributes (ARIA labels, roles, etc.)
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": api_key
            }
        ],
        "temperature": 0.7,
    }
    
    agent = autogen.ConversableAgent(
        name="ui_design_expert",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    # Register design tools
    @agent.register_for_llm(description="Generate a color palette based on brand color")
    def generate_color_palette(base_color: str, style: str = "modern") -> Dict[str, str]:
        """Generate a complete color palette."""
        # This would use actual color theory algorithms
        return {
            "primary": base_color,
            "secondary": "#10B981",
            "accent": "#F59E0B",
            "background": "#F9FAFB",
            "text": "#1F2937",
            "border": "#E5E7EB",
        }
    
    @agent.register_for_execution()
    def generate_color_palette(base_color: str, style: str = "modern") -> Dict[str, str]:
        return {
            "primary": base_color,
            "secondary": "#10B981",
            "accent": "#F59E0B",
            "background": "#F9FAFB",
            "text": "#1F2937",
            "border": "#E5E7EB",
        }
    
    return agent


def create_accessibility_checker_agent() -> autogen.ConversableAgent:
    """
    Create an agent that checks UI components for accessibility issues.
    """
    
    system_message = """You are an Accessibility Expert Agent. Your role is to
    ensure all UI components are accessible to all users, including those
    with disabilities.
    
    Check for:
    - Proper ARIA attributes
    - Keyboard navigation support
    - Color contrast ratios (WCAG AA: 4.5:1 for text)
    - Screen reader compatibility
    - Focus indicators
    - Alternative text for images
    - Semantic HTML structure
    
    Provide specific recommendations for improvements.
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": api_key
            }
        ],
        "temperature": 0.5,
    }
    
    return autogen.ConversableAgent(
        name="accessibility_checker",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )


# Example usage
if __name__ == "__main__":
    design_agent = create_ui_design_agent()
    a11y_agent = create_accessibility_checker_agent()
    
    print("UI Design and Accessibility agents created!")
    print("These agents ensure beautiful and accessible UI generation.")
