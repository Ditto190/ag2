# AG2 Generative UI Development Container

This devcontainer is specifically configured for building **Generative UI applications** that integrate **AG2 agentic AI** workflows.

## What's Included

### Development Tools
- **Python 3.11**: For AG2 agent development
- **Node.js 20**: For modern frontend development
- **pnpm**: Fast, disk space-efficient package manager
- **TypeScript**: Type-safe JavaScript development

### Python Libraries
- **AG2 (AutoGen)**: Multi-agent framework with full features
- **FastAPI**: High-performance async web framework
- **Uvicorn**: ASGI server for production-ready deployments
- **Pydantic**: Data validation and settings management
- **WebSockets**: Real-time bidirectional communication

### VS Code Extensions
- Python development tools (Pylance, Black formatter)
- JavaScript/TypeScript tools (ESLint, Prettier)
- React development support
- Tailwind CSS IntelliSense

### Port Forwarding
- **Port 3000**: Frontend development server (Next.js/React)
- **Port 8000**: Backend API server (FastAPI)

## Quick Start

1. **Open in GitHub Codespaces**
   - Click the green "Code" button
   - Select "Codespaces" tab
   - Choose "AG2 Generative UI Development" template

2. **Set your API keys** (optional but recommended)
   - During codespace creation, add your `OPENAI_API_KEY`
   - Or set them later as environment variables

3. **Navigate to the template**
   ```bash
   cd templates/generative-ui
   ```

4. **Follow the template README** to build your first Generative UI app

## What is Generative UI?

Generative UI is an emerging pattern where AI agents dynamically generate and stream user interface components based on user interactions and context. Instead of static UI flows, the interface adapts in real-time to provide contextual, personalized experiences.

### Key Concepts

- **Dynamic Component Generation**: AI agents decide which UI components to render
- **Streaming Interfaces**: UI updates progressively as AI generates responses
- **Agentic Workflows**: Multiple specialized agents collaborate to fulfill user requests
- **Type-Safe Communication**: Structured data flow between agents and UI

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js/React)         │
│  ┌────────────────────────────────────────────┐    │
│  │  Generative UI Components                  │    │
│  │  - Dynamic rendering based on AI responses │    │
│  │  - Streaming updates from agents           │    │
│  └────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │ WebSocket/HTTP
┌─────────────────▼───────────────────────────────────┐
│              Backend (FastAPI)                       │
│  ┌────────────────────────────────────────────┐    │
│  │  AG2 Multi-Agent System                    │    │
│  │  - Orchestrate specialized agents          │    │
│  │  - Tool calling and execution              │    │
│  │  - Structured output generation            │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## Example Use Cases

- **Conversational Dashboards**: Data visualization that adapts based on questions
- **Interactive Assistants**: Multi-step workflows with dynamic form generation
- **Content Creation Tools**: AI-powered editors with real-time suggestions
- **Research Interfaces**: Complex multi-agent research with progressive disclosure

## Resources

- [AG2 Documentation](https://docs.ag2.ai/)
- [AG2 GitHub](https://github.com/ag2ai/ag2)
- [Build with AG2 Examples](https://github.com/ag2ai/build-with-ag2)

## Support

For issues or questions:
- [AG2 Discord](https://discord.gg/pAbnFJrkgZ)
- [GitHub Issues](https://github.com/ag2ai/ag2/issues)
