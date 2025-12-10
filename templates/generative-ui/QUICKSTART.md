# AG2 Generative UI Template

## Quick Start Guide

### Prerequisites

- Python 3.11+
- Node.js 20+
- OpenAI API key (or other LLM provider)

### Installation

1. **Clone and navigate to the template**
   ```bash
   cd templates/generative-ui
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   
   # Install dependencies
   pnpm install  # or npm install
   
   # Set up environment
   cp .env.example .env.local
   ```

4. **Start the development servers**

   Terminal 1 (Backend):
   ```bash
   cd backend
   python main.py
   ```

   Terminal 2 (Frontend):
   ```bash
   cd frontend
   pnpm dev
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:3000`

### Your First Generative UI

Try these example queries:

- "Create a card showing company information"
- "Build a table with sample sales data"
- "Show me an alert about system maintenance"
- "Generate a dashboard for project metrics"

### Customization

#### Add New UI Components

1. Create a new component in `frontend/components/dynamic/`
2. Add it to the component map in `DynamicComponent.tsx`

Example:
```typescript
// frontend/components/dynamic/Chart.tsx
export function Chart({ title, data }: ChartProps) {
  // Your chart implementation
}

// frontend/components/dynamic/DynamicComponent.tsx
import { Chart } from './Chart';

const componentMap = {
  // ... existing components
  chart: Chart,
};
```

#### Add New Agents

1. Create a new agent in `backend/agents/`
2. Add it to the group chat in `orchestrator.py`

Example:
```python
# backend/agents/custom_agent.py
from autogen import ConversableAgent, LLMConfig

def create_custom_agent(llm_config: LLMConfig) -> ConversableAgent:
    return ConversableAgent(
        name="custom_agent",
        system_message="Your custom system message",
        llm_config=llm_config,
    )
```

#### Modify Agent Behavior

Edit the system messages in `backend/agents/orchestrator.py`:

```python
def create_ui_generator_agent(llm_config: LLMConfig) -> ConversableAgent:
    system_message = """Your custom instructions here"""
    # ... rest of the function
```

### Project Structure

```
generative-ui/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── agents/
│   │   └── orchestrator.py        # Multi-agent workflow
│   ├── schemas/
│   │   └── messages.py            # Pydantic models
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Home page
│   │   └── globals.css
│   ├── components/
│   │   ├── GenerativeUIChat.tsx   # Main chat interface
│   │   └── dynamic/               # Dynamic UI components
│   │       ├── DynamicComponent.tsx
│   │       ├── Card.tsx
│   │       ├── Alert.tsx
│   │       └── DataTable.tsx
│   ├── package.json
│   └── .env.example
└── README.md
```

### API Documentation

Once the backend is running, visit:
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### Troubleshooting

**Backend won't start**
- Check your API key is set in `.env`
- Ensure Python 3.11+ is installed
- Verify all dependencies are installed

**Frontend won't connect**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify `.env.local` has correct API URLs

**Agents not responding**
- Check API key validity
- Review agent system messages
- Check console logs for errors

### Next Steps

1. Explore the example queries
2. Customize the UI components
3. Add new agent capabilities
4. Integrate with your data sources
5. Deploy to production

### Resources

- [AG2 Documentation](https://docs.ag2.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

### Support

- [AG2 Discord](https://discord.gg/pAbnFJrkgZ)
- [GitHub Issues](https://github.com/ag2ai/ag2/issues)
