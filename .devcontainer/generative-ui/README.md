# AG2 Generative UI Devcontainer

This devcontainer provides a complete development environment for building Generative UI applications with AG2 and the Model Context Protocol (MCP).

## Overview

The Generative UI devcontainer integrates:

- **AG2 Framework**: Multi-agent orchestration and conversation management
- **MCP Protocol**: Standardized tool orchestration for LLM agents
- **Data Grounding**: Real-time data retrieval for factual UI generation
- **Development Tools**: Pre-configured Python environment with all dependencies

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│              (Generative UI Components)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                        │
│  • AG2 Agents (AssistantAgent, UserProxyAgent)             │
│  • Conversation Management                                  │
│  • Tool Routing & Execution                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Tooling & Hydration Layer (MCP)                │
│  • ArXiv: Academic paper search & retrieval                 │
│  • Wikipedia: Encyclopedia content access                   │
│  • Filesystem: Document & context file access               │
│  • Custom: Domain-specific tools                            │
└─────────────────────────────────────────────────────────────┘
```

## Features

### ✨ Key Capabilities

- **MCP Integration**: Out-of-the-box MCP servers for common data sources
- **Multi-Agent Support**: Coordinate multiple AG2 agents with shared tools
- **Search-First Architecture**: Retrieve real data before rendering UI
- **Extensible**: Easy addition of custom MCP servers for domain-specific needs
- **Development Ready**: Pre-configured environment with all dependencies

### 🔧 Included MCP Servers

1. **ArXiv Server**: Search and retrieve academic papers
2. **Wikipedia Server**: Search and retrieve encyclopedia articles
3. **Filesystem Server**: Sandboxed access to context documents

### 📦 Pre-installed Dependencies

- AG2 with MCP support (`ag2[openai,mcp,mcp-proxy-gen]`)
- MCP client and server libraries
- ArXiv and Wikipedia API clients
- FastAPI and Uvicorn for SSE transport
- Development tools (pytest, pre-commit, etc.)

## Getting Started

### Prerequisites

- Visual Studio Code with Dev Containers extension, OR
- GitHub Codespaces account, OR
- Docker and VS Code Remote Containers

### Option 1: Using Codespaces

1. Navigate to the repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Select the "AG2 Generative UI with MCP" devcontainer
4. Wait for the container to build and initialize

### Option 2: Local Development

1. Open the repository in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Select "Dev Containers: Reopen in Container"
4. Choose "AG2 Generative UI with MCP"
5. Wait for the container to build

### Configuration

Set up your API keys (optional but recommended):

```bash
# In the devcontainer terminal
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"  # Optional
export GEMINI_API_KEY="your-gemini-key"  # Optional
```

Or create a `.env` file in the workspace root:

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GEMINI_API_KEY=your-gemini-key
```

## Quick Start Examples

### Example 1: Basic MCP Client

```bash
cd .devcontainer/generative-ui/mcp/examples
python mcp_client_example.py
```

This demonstrates:
- Connecting to an MCP server
- Creating a toolkit from MCP tools
- Calling tools directly

### Example 2: MCP Toolkit Demo

```bash
cd .devcontainer/generative-ui/mcp/examples
python mcp_toolkit_demo.py
```

This demonstrates:
- Toolkit inspection and introspection
- Working with multiple toolkits
- Error handling patterns

### Example 3: Generative UI with MCP

```bash
cd .devcontainer/generative-ui/mcp/examples
export OPENAI_API_KEY="your-key"
python genui_with_mcp.py
```

This demonstrates:
- Full AG2 agent integration
- Multi-server coordination
- Grounding UI generation in real data

## MCP Server Management

### Starting Servers

**Stdio Mode (default for examples)**:
```bash
cd .devcontainer/generative-ui/mcp
bash run_mcp_servers.sh stdio
```

**SSE Mode (for multi-client scenarios)**:
```bash
cd .devcontainer/generative-ui/mcp
bash run_mcp_servers.sh sse
```

This starts all MCP servers in the background on ports 8000-8002.

### Stopping Servers

```bash
# Get PIDs from the saved file
cd .devcontainer/generative-ui/mcp
cat .mcp_server_pids
kill $(cat .mcp_server_pids)
```

### Starting Individual Servers

```bash
# ArXiv (stdio)
python mcp/servers/mcp_arxiv.py stdio --storage-path ./mcp/storage/papers

# ArXiv (SSE on port 8000)
python mcp/servers/mcp_arxiv.py sse --storage-path ./mcp/storage/papers

# Filesystem
python mcp/servers/mcp_filesystem.py stdio --context-path ./mcp/context_docs

# Wikipedia
python mcp/servers/mcp_wikipedia.py stdio --storage-path ./mcp/storage/articles
```

## Project Structure

```
.devcontainer/generative-ui/
├── devcontainer.json              # Devcontainer configuration
├── setup.sh                       # Environment setup script
├── README.md                      # This file
└── mcp/                          # MCP integration layer
    ├── README.md                 # MCP documentation
    ├── servers/                  # MCP server implementations
    │   ├── mcp_arxiv.py
    │   ├── mcp_filesystem.py
    │   ├── mcp_wikipedia.py
    │   └── mcp_server_template.py
    ├── examples/                 # Integration examples
    │   ├── genui_with_mcp.py
    │   ├── mcp_client_example.py
    │   └── mcp_toolkit_demo.py
    ├── utils/                    # Helper utilities
    │   └── mcp_helpers.py
    ├── storage/                  # Server data storage
    │   ├── papers/              # ArXiv papers
    │   └── articles/            # Wikipedia articles
    ├── context_docs/            # Filesystem server context
    └── run_mcp_servers.sh       # Server management script
```

## Use Cases

### 1. Research Paper Browser

Build a UI that searches arXiv and displays papers with their metadata:

```python
# Search for papers
papers = await search_arxiv("transformers", max_results=5)

# Get details for each paper
for paper_id in papers:
    info = await get_paper_info(paper_id)
    # Generate UI card component with paper info
```

### 2. Knowledge Base Explorer

Combine Wikipedia and custom documents to create a rich knowledge interface:

```python
# Get background from Wikipedia
wiki_summary = await get_article_summary("Machine Learning")

# Get internal docs
internal_docs = await list_files("ml_guides/")

# Generate navigation UI combining both sources
```

### 3. Contextual Documentation Assistant

Ground AI responses in your project's documentation:

```python
# Search project docs
docs = await read_file("api_docs.md")

# Use context to generate accurate API usage examples
# Agent has access to real documentation
```

## Extending the System

### Adding a Custom MCP Server

1. Use the template:
```bash
cp mcp/servers/mcp_server_template.py mcp/servers/mcp_myservice.py
```

2. Implement your tools:
```python
@mcp.tool()
def my_custom_tool(param: str) -> dict:
    """Tool description for the LLM."""
    # Your implementation
    return {"result": "data"}
```

3. Add to `run_mcp_servers.sh`:
```bash
python servers/mcp_myservice.py sse --config-param value &
```

4. Document in `mcp/README.md`

### Creating Integration Examples

Add new examples to `mcp/examples/` showing:
- How to connect to your server
- Common usage patterns
- Integration with AG2 agents
- UI generation scenarios

## Best Practices

### Security

- ✅ Use environment variables for API keys
- ✅ Restrict filesystem server paths
- ✅ Validate all user inputs in custom servers
- ✅ Use HTTPS for production SSE servers
- ✅ Implement rate limiting for expensive operations

### Performance

- ✅ Reuse MCP sessions across multiple calls
- ✅ Use async/await for concurrent operations
- ✅ Implement caching for frequently accessed data
- ✅ Set appropriate result limits
- ✅ Close sessions properly to free resources

### Development

- ✅ Start with stdio transport for simplicity
- ✅ Test servers independently before integration
- ✅ Use type hints for better IDE support
- ✅ Write comprehensive tool docstrings
- ✅ Add error handling for all tool operations

## Troubleshooting

### Server Connection Issues

```bash
# Test if server is running
python -c "import asyncio; from autogen.mcp.mcp_client import *; asyncio.run(test_connection())"

# Check logs
python mcp/servers/mcp_arxiv.py stdio --storage-path ./papers 2>&1 | tee error.log
```

### Port Conflicts (SSE mode)

```bash
# Find what's using the port
lsof -i :8000

# Use a different port
python mcp/servers/mcp_arxiv.py sse --storage-path ./papers --port 8010
```

### Import Errors

```bash
# Reinstall dependencies
pip install -e ".[dev,openai,mcp,mcp-proxy-gen]"
pip install arxiv wikipedia-api fastapi uvicorn
```

## Resources

### Documentation

- [MCP Integration Guide](./mcp/README.md) - Detailed MCP documentation
- [AG2 Documentation](https://docs.ag2.ai) - Full AG2 framework docs
- [MCP Protocol](https://modelcontextprotocol.io/) - MCP specification

### Examples

- [Basic Examples](./mcp/examples/) - Getting started code
- [Notebook Examples](../../../notebook/mcp/) - Interactive notebooks
- [AG2 Examples](../../../notebook/) - Full AG2 example collection

### Community

- [AG2 GitHub](https://github.com/ag2ai/ag2) - Source code and issues
- [AG2 Discussions](https://github.com/ag2ai/ag2/discussions) - Community Q&A

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

Please follow the existing code style and add appropriate documentation for any new features.

## License

This project is part of the AG2 framework and is licensed under the Apache License 2.0.

## Support

For help and support:
- Check the [troubleshooting section](#troubleshooting)
- Review the [MCP documentation](./mcp/README.md)
- Open an issue on [GitHub](https://github.com/ag2ai/ag2/issues)
- Join the community discussions
