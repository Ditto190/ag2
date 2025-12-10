# Example Use Cases for AG2 Generative UI

This directory contains example implementations demonstrating various use cases for the Generative UI template.

## Available Examples

### 1. Chat Interface (`chat-interface.py`)
A simple conversational interface where agents generate appropriate UI components based on user messages.

**Use Case**: Customer support chatbot with dynamic form generation

**Try it**:
```python
python examples/chat-interface.py
```

**Example queries**:
- "I need to report a bug"
- "Show me my account information"
- "Create a feedback form"

### 2. Data Dashboard (`data-dashboard.py`)
Demonstrates how agents can generate data visualizations and analytics dashboards on demand.

**Use Case**: Business intelligence tool with natural language queries

**Try it**:
```python
python examples/data-dashboard.py
```

**Example queries**:
- "Show me sales performance for Q4"
- "Create a comparison chart of revenue vs expenses"
- "Display top 10 customers by revenue"

### 3. Form Builder (`form-builder.py`)
Showcases dynamic form generation based on natural language descriptions.

**Use Case**: No-code form creation tool

**Try it**:
```python
python examples/form-builder.py
```

**Example queries**:
- "Create a customer registration form"
- "Build a product feedback survey"
- "Generate an event booking form"

### 4. Research Assistant (`research-assistant.py`)
Multi-agent system that researches topics and presents findings with rich UI components.

**Use Case**: Academic research tool with progressive disclosure

**Try it**:
```python
python examples/research-assistant.py
```

**Example queries**:
- "Research the history of artificial intelligence"
- "Compare Python and JavaScript for web development"
- "Explain quantum computing"

## Creating Your Own Examples

1. Copy an existing example as a starting point
2. Modify the agent system messages for your use case
3. Define custom UI components if needed
4. Test your implementation

### Example Structure

```python
from autogen import ConversableAgent, LLMConfig

# Define specialized agents
agent1 = ConversableAgent(
    name="agent1",
    system_message="Your custom instructions",
    llm_config=llm_config,
)

# Create workflow
# Generate UI components
# Return results
```

## Integration with Frontend

All examples work with the default frontend. Components are automatically rendered based on their type:

- `card`: Information display
- `table`: Tabular data
- `alert`: Notifications
- `chart`: Visualizations (requires custom component)
- `form`: Input collection (requires custom component)

## Best Practices

1. **Clear Agent Roles**: Each agent should have a specific, well-defined purpose
2. **Structured Output**: Always return valid JSON component definitions
3. **Error Handling**: Include validation and error messages
4. **Progressive Disclosure**: Break complex information into digestible components
5. **User Feedback**: Provide loading states and confirmation messages

## Contributing

Have an interesting use case? Submit a PR with your example!

Requirements:
- Working code with comments
- README section describing the use case
- Example queries demonstrating functionality
