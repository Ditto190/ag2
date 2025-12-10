# Getting Started with AG2 Generative UI

Welcome! This guide will help you get started with building **Generative UI applications** using the **AG2 multi-agent framework**.

## What You'll Build

By following this guide, you'll create an AI-powered application where:
- Agents dynamically generate UI components based on user input
- Multiple specialized agents collaborate to fulfill requests
- The interface adapts in real-time to provide contextual experiences
- All communication is type-safe and structured

## Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.11+** installed
- ✅ **Node.js 20+** installed
- ✅ **OpenAI API key** (or another LLM provider)
- ✅ Basic knowledge of Python and JavaScript/TypeScript

## Quick Start (5 minutes)

### Step 1: Set Up Your Environment

If you're using the **Generative UI devcontainer** in GitHub Codespaces, this is already done! Otherwise:

```bash
# Navigate to the template
cd templates/generative-ui

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend (in a new terminal)
cd ../frontend
pnpm install  # or npm install
```

### Step 2: Configure API Keys

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Frontend
cd ../frontend
cp .env.example .env.local
```

### Step 3: Start the Servers

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev
```

### Step 4: Open Your Browser

Navigate to `http://localhost:3000` and try these queries:

- "Create a card showing company information"
- "Build a table with sample sales data"
- "Show me an alert about system maintenance"

🎉 **Congratulations!** You've just created your first Generative UI application!

## Understanding the Architecture

### Backend (Python + AG2)

```
backend/
├── main.py              # FastAPI server with WebSocket support
├── agents/
│   └── orchestrator.py  # Multi-agent workflow coordination
├── schemas/
│   └── messages.py      # Type-safe data models
└── utils/
    └── helpers.py       # Utility functions
```

**Key Concepts:**

1. **Orchestrator Agent**: Coordinates the overall workflow
2. **UI Generator Agent**: Creates structured component definitions
3. **Data Agent**: Handles data fetching and processing
4. **Group Chat**: Enables multi-agent collaboration

### Frontend (Next.js + React)

```
frontend/
├── app/
│   ├── page.tsx         # Main application page
│   └── layout.tsx       # Root layout
├── components/
│   ├── GenerativeUIChat.tsx  # Chat interface
│   └── dynamic/              # Dynamic UI components
│       ├── Card.tsx
│       ├── Alert.tsx
│       └── DataTable.tsx
```

**Key Concepts:**

1. **Dynamic Components**: Render based on agent responses
2. **Type Safety**: TypeScript ensures correct component usage
3. **Real-time Updates**: WebSocket support for streaming
4. **Component Mapping**: Automatically selects the right component

## Your First Customization

Let's add a custom UI component!

### 1. Create the Component

Create `frontend/components/dynamic/Metric.tsx`:

```typescript
interface MetricProps {
  title: string;
  value: string;
  change?: string;
  trend?: 'up' | 'down';
}

export function Metric({ title, value, change, trend }: MetricProps) {
  return (
    <div className="bg-white border rounded-lg p-4">
      <h3 className="text-sm text-gray-600">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      {change && (
        <p className={`text-sm ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
          {change}
        </p>
      )}
    </div>
  );
}
```

### 2. Register the Component

Edit `frontend/components/dynamic/DynamicComponent.tsx`:

```typescript
import { Metric } from './Metric';

const componentMap = {
  card: Card,
  alert: Alert,
  table: DataTable,
  metric: Metric,  // Add this line
};
```

### 3. Update the Agent

Edit `backend/agents/orchestrator.py` and add to the UI generator's system message:

```python
Available component types:
- card: Information display
- chart: Data visualization
- table: Tabular data
- form: Input collection
- list: Ordered or unordered items
- alert: Important messages
- metric: KPI/metric display  # Add this line
```

### 4. Test It!

Restart the backend and try: "Show me a metric for monthly revenue"

## Common Patterns

### Pattern 1: Multi-Step Workflows

```python
# Agent asks clarifying questions
user: "I want to create a report"
agent: "What type of report? (sales, inventory, customer)"
user: "sales"
agent: [generates sales report UI]
```

### Pattern 2: Progressive Disclosure

```python
# Start simple, add detail on demand
user: "Show sales data"
agent: [generates summary card]
user: "Show more details"
agent: [generates detailed table]
user: "Visualize the trend"
agent: [generates chart]
```

### Pattern 3: Conditional Components

```python
# Different UI based on context
if user.role == "admin":
    return [admin_dashboard, user_management]
else:
    return [user_dashboard]
```

## Troubleshooting

### Issue: Agents Not Responding

**Solution:**
1. Check your API key in `.env`
2. Verify the backend is running on port 8000
3. Check browser console for errors
4. Review backend logs for exceptions

### Issue: Components Not Rendering

**Solution:**
1. Ensure component type matches the registered name
2. Check the component prop structure
3. Verify JSON format from agents
4. Look for console errors in the browser

### Issue: WebSocket Connection Failed

**Solution:**
1. Verify backend is running
2. Check CORS settings in `main.py`
3. Ensure WebSocket URL is correct in frontend `.env.local`

## Next Steps

Now that you have the basics, explore:

1. **[Examples](examples/README.md)** - See real-world use cases
2. **[Full README](README.md)** - Comprehensive documentation
3. **[QUICKSTART](QUICKSTART.md)** - Detailed setup guide
4. **[AG2 Docs](https://docs.ag2.ai/)** - Learn more about AG2

## Learning Resources

- **AG2 Documentation**: https://docs.ag2.ai/
- **Multi-Agent Patterns**: https://docs.ag2.ai/workflows
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Next.js Documentation**: https://nextjs.org/docs

## Get Help

- 💬 [AG2 Discord](https://discord.gg/pAbnFJrkgZ)
- 🐛 [GitHub Issues](https://github.com/ag2ai/ag2/issues)
- 📖 [AG2 Documentation](https://docs.ag2.ai/)

## What's Next?

Choose your path:

- **🎨 Frontend Developer?** → Explore custom components and styling
- **🤖 AI Engineer?** → Deep dive into agent design and tools
- **📊 Data Scientist?** → Build analytics and visualization agents
- **🏗️ Full-Stack?** → Create end-to-end applications

Happy building! 🚀
