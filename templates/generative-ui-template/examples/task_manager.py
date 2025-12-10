"""
Example Application: Task Manager with Generative UI

This example demonstrates how to build a complete application using
the Generative UI template with AG2 agents.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents import create_coordinator_agent, create_ui_agent, create_data_agent
from backend.ui_generator import UIGenerator


class TaskManagerApp:
    """
    Example task manager application using Generative UI.
    
    This app demonstrates:
    - Dynamic form generation for task creation
    - Data tables for task lists
    - Dashboard for task analytics
    - Agent-driven UI adaptation
    """
    
    def __init__(self):
        self.coordinator = create_coordinator_agent()
        self.ui_agent = create_ui_agent()
        self.data_agent = create_data_agent()
        self.ui_generator = UIGenerator()
        
        # Mock task data
        self.tasks = [
            {"id": 1, "title": "Design Homepage", "status": "In Progress", "priority": "High"},
            {"id": 2, "title": "Setup Database", "status": "Complete", "priority": "High"},
            {"id": 3, "title": "Write Tests", "status": "Todo", "priority": "Medium"},
        ]
    
    def generate_task_form(self):
        """Generate a form for creating new tasks."""
        intent = "Create a form for adding a new task with title, description, priority, and deadline"
        
        ui_spec = self.ui_generator.generate(
            intent=intent,
            context={"purpose": "task_creation"},
            agents={
                "coordinator": self.coordinator,
                "ui_agent": self.ui_agent
            }
        )
        
        # Customize the generated form
        ui_spec["fields"] = [
            {
                "name": "title",
                "label": "Task Title",
                "type": "text",
                "required": True,
                "placeholder": "Enter task title"
            },
            {
                "name": "description",
                "label": "Description",
                "type": "textarea",
                "required": False,
                "placeholder": "Describe the task..."
            },
            {
                "name": "priority",
                "label": "Priority",
                "type": "select",
                "required": True,
                "options": ["Low", "Medium", "High", "Critical"]
            },
            {
                "name": "deadline",
                "label": "Deadline",
                "type": "date",
                "required": False
            }
        ]
        
        return ui_spec
    
    def generate_task_list(self):
        """Generate a table view of tasks."""
        intent = "Show a table of all tasks with their details"
        
        ui_spec = self.ui_generator.generate(
            intent=intent,
            context={"data": self.tasks},
            agents={
                "coordinator": self.coordinator,
                "ui_agent": self.ui_agent,
                "data_agent": self.data_agent
            }
        )
        
        # Use actual task data
        ui_spec["headers"] = ["ID", "Title", "Status", "Priority"]
        ui_spec["rows"] = [
            [str(task["id"]), task["title"], task["status"], task["priority"]]
            for task in self.tasks
        ]
        
        return ui_spec
    
    def generate_task_dashboard(self):
        """Generate a dashboard with task analytics."""
        intent = "Create a dashboard showing task statistics and metrics"
        
        # Calculate metrics
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["status"] == "Complete")
        in_progress = sum(1 for t in self.tasks if t["status"] == "In Progress")
        todo = sum(1 for t in self.tasks if t["status"] == "Todo")
        
        ui_spec = self.ui_generator.generate(
            intent=intent,
            context={"metrics": {"total": total_tasks, "completed": completed}},
            agents={
                "coordinator": self.coordinator,
                "ui_agent": self.ui_agent
            }
        )
        
        # Customize with real metrics
        ui_spec["widgets"] = [
            {
                "type": "metric",
                "title": "Total Tasks",
                "value": str(total_tasks),
                "change": "+3 this week",
                "trend": "up"
            },
            {
                "type": "metric",
                "title": "Completed",
                "value": str(completed),
                "change": f"{(completed/total_tasks*100):.0f}%",
                "trend": "up"
            },
            {
                "type": "metric",
                "title": "In Progress",
                "value": str(in_progress),
                "change": "",
                "trend": "neutral"
            },
            {
                "type": "metric",
                "title": "To Do",
                "value": str(todo),
                "change": "",
                "trend": "neutral"
            }
        ]
        
        return ui_spec
    
    def process_user_intent(self, user_input: str):
        """
        Process natural language user input to determine what UI to show.
        
        This demonstrates how agents can interpret user intent and
        generate appropriate UI responses.
        """
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["add", "create", "new task"]):
            return self.generate_task_form()
        
        elif any(word in user_input_lower for word in ["list", "show tasks", "view tasks"]):
            return self.generate_task_list()
        
        elif any(word in user_input_lower for word in ["dashboard", "overview", "statistics"]):
            return self.generate_task_dashboard()
        
        else:
            # Default: show options
            return {
                "type": "card",
                "title": "Task Manager",
                "content": "What would you like to do?",
                "actions": [
                    {"label": "Add Task", "intent": "create new task"},
                    {"label": "View Tasks", "intent": "show all tasks"},
                    {"label": "Dashboard", "intent": "show dashboard"}
                ]
            }


def main():
    """Run example application."""
    print("=" * 60)
    print("Task Manager - Generative UI Example")
    print("=" * 60)
    
    app = TaskManagerApp()
    
    print("\n1. Generating Task Form...")
    task_form = app.generate_task_form()
    print(f"   Type: {task_form['type']}")
    print(f"   Fields: {len(task_form.get('fields', []))}")
    
    print("\n2. Generating Task List...")
    task_list = app.generate_task_list()
    print(f"   Type: {task_list['type']}")
    print(f"   Rows: {len(task_list.get('rows', []))}")
    
    print("\n3. Generating Dashboard...")
    dashboard = app.generate_task_dashboard()
    print(f"   Type: {dashboard['type']}")
    print(f"   Widgets: {len(dashboard.get('widgets', []))}")
    
    print("\n4. Processing Natural Language Intent...")
    intents = [
        "I want to add a new task",
        "Show me all my tasks",
        "Give me an overview"
    ]
    
    for intent in intents:
        ui_response = app.process_user_intent(intent)
        print(f"   Intent: '{intent}' → UI Type: {ui_response['type']}")
    
    print("\n" + "=" * 60)
    print("Example complete! This demonstrates how agents generate")
    print("different UIs based on user intent and application context.")
    print("=" * 60)


if __name__ == "__main__":
    main()
