# AG2 Generative UI Template

A production-ready template for building **Generative UI applications** powered by **AG2 multi-agent AI**.

## Overview

This template provides a complete framework for creating dynamic, AI-powered user interfaces where agents generate UI components in real-time based on user interactions and context.

## Architecture

```
generative-ui/
├── backend/          # FastAPI server with AG2 agents
│   ├── main.py      # API server and WebSocket endpoints
│   ├── agents/      # AG2 agent definitions
│   └── schemas/     # Pydantic models for type safety
├── frontend/         # Next.js application
│   ├── app/         # Next.js 14 app directory
│   ├── components/  # React components
│   └── lib/         # Utilities and API clients
└── shared/          # Shared types and utilities
```

## Quick Start

### 1. Set up environment

```bash
# Create .env file
cp .env.example .env

# Add your OpenAI API key
echo "OPENAI_API_KEY=sk-..." >> .env
```

### 2. Start the backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend will run on `http://localhost:8000`

### 3. Start the frontend

```bash
cd frontend
pnpm install
pnpm dev
```

The frontend will run on `http://localhost:3000`

## Features

### 🤖 Multi-Agent Architecture
- **Orchestrator Agent**: Coordinates workflow and agent selection
- **UI Generator Agent**: Creates dynamic React components
- **Data Agent**: Fetches and processes data
- **Formatter Agent**: Structures responses for UI consumption

### 🎨 Dynamic UI Components
- Streaming text responses
- Dynamic form generation
- Real-time data visualizations
- Interactive cards and panels
- Progressive disclosure

### 🔄 Real-Time Communication
- WebSocket support for bi-directional streaming
- HTTP endpoints for stateless requests
- Structured JSON responses
- Type-safe data transfer

### 🛡️ Type Safety
- TypeScript frontend
- Pydantic backend models
- Shared type definitions
- Runtime validation

## Example: Building a Research Assistant

```python
# backend/agents/research_agent.py
from autogen import ConversableAgent, GroupChat, GroupChatManager, LLMConfig

llm_config = LLMConfig.from_env()

# Define specialized agents
researcher = ConversableAgent(
    name="researcher",
    system_message="Research topics and gather information.",
    llm_config=llm_config,
)

summarizer = ConversableAgent(
    name="summarizer",
    system_message="Create concise summaries of research findings.",
    llm_config=llm_config,
)

ui_generator = ConversableAgent(
    name="ui_generator",
    system_message="""Generate UI components in JSON format.
    Return: {"type": "card", "title": "...", "content": "..."}""",
    llm_config=llm_config,
)

# Create group chat
group_chat = GroupChat(
    agents=[researcher, summarizer, ui_generator],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

```typescript
// frontend/components/GenerativeUI.tsx
'use client';

import { useState } from 'react';
import { useGenerativeUI } from '@/lib/hooks/useGenerativeUI';

export default function GenerativeUI() {
  const [query, setQuery] = useState('');
  const { components, isStreaming, sendMessage } = useGenerativeUI();

  return (
    <div className="space-y-4">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            sendMessage(query);
            setQuery('');
          }
        }}
        placeholder="Ask me anything..."
        className="w-full p-3 border rounded-lg"
      />
      
      <div className="space-y-4">
        {components.map((component, i) => (
          <DynamicComponent key={i} {...component} />
        ))}
      </div>
      
      {isStreaming && <LoadingIndicator />}
    </div>
  );
}
```

## API Reference

### WebSocket Endpoint

```
ws://localhost:8000/ws/generate
```

**Message Format:**
```json
{
  "query": "Analyze sales data for Q4",
  "context": {},
  "stream": true
}
```

**Response Format:**
```json
{
  "type": "component",
  "component": {
    "type": "card",
    "title": "Q4 Sales Analysis",
    "content": "...",
    "data": {}
  }
}
```

### HTTP Endpoints

- `POST /api/generate` - Generate UI components
- `GET /api/health` - Health check
- `POST /api/chat` - Chat with agents

## Advanced Usage

### Custom Agent Tools

```python
from typing import Annotated
from autogen import register_function

def fetch_sales_data(
    quarter: Annotated[str, "Quarter in format Q1, Q2, etc."]
) -> dict:
    # Your data fetching logic
    return {"revenue": 1000000, "growth": 15}

register_function(
    fetch_sales_data,
    caller=orchestrator_agent,
    executor=data_agent,
    description="Fetch sales data for analysis"
)
```

### Streaming Responses

```python
async def stream_response(query: str):
    async for chunk in agent_workflow(query):
        yield {
            "type": "stream",
            "content": chunk
        }
```

### Custom UI Components

```typescript
// Add to frontend/components/dynamic/index.ts
export const componentMap = {
  card: Card,
  chart: Chart,
  table: Table,
  form: DynamicForm,
  // Add your custom components
};
```

## Configuration

### Backend (.env)

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MODEL_NAME=gpt-4o-mini
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Frontend (next.config.js)

```javascript
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
pnpm test
```

## Deployment

### Backend (Docker)

```bash
cd backend
docker build -t ag2-backend .
docker run -p 8000:8000 ag2-backend
```

### Frontend (Vercel)

```bash
cd frontend
vercel deploy
```

## Best Practices

1. **Agent Design**
   - Keep agents focused on single responsibilities
   - Use clear system messages
   - Implement proper error handling

2. **UI Components**
   - Make components stateless when possible
   - Use TypeScript for type safety
   - Implement loading and error states

3. **Performance**
   - Stream responses for better UX
   - Implement caching strategies
   - Use WebSockets for real-time features

4. **Security**
   - Validate all inputs
   - Sanitize AI-generated content
   - Use environment variables for secrets

## Examples

See the `examples/` directory for complete implementations:
- `examples/chat-interface/` - Basic conversational UI
- `examples/data-dashboard/` - Analytics dashboard
- `examples/form-builder/` - Dynamic form generation
- `examples/research-assistant/` - Multi-agent research tool

## Troubleshooting

### Connection Issues

If WebSocket connection fails:
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Check WebSocket endpoint
wscat -c ws://localhost:8000/ws/generate
```

### Agent Configuration

If agents aren't responding:
- Verify API keys in `.env`
- Check LLM configuration
- Review agent system messages

## Contributing

Contributions are welcome! See the main [AG2 Contributing Guide](../../CONTRIBUTING.md).

## Resources

- [AG2 Documentation](https://docs.ag2.ai/)
- [Generative UI Patterns](https://docs.ag2.ai/patterns/generative-ui)
- [Multi-Agent Workflows](https://docs.ag2.ai/workflows)

## License

Apache 2.0 - See [LICENSE](../../LICENSE)
