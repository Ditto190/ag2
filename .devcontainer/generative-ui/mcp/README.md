# MCP Integration for AG2 Generative UI

This directory contains the Model Context Protocol (MCP) integration layer for AG2's Generative UI architecture. MCP enables standardized tool orchestration, external data retrieval, and agent-to-service communication for building data-grounded generative UIs.

## Overview

The MCP integration provides:

- **Tool Orchestration**: Standardized protocol for exposing tools to LLM agents
- **Data Grounding**: Real-time retrieval of factual data to ground UI generation
- **Search-First Architecture**: Retrieve real data before rendering UI components
- **Modular Services**: Easy addition of custom MCP servers for domain-specific tools

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Generative UI Layer                        │
│  (CopilotKit, AG2 Agents, UI Components)               │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│         MCP Orchestration Layer                         │
│  • Toolkit Management                                   │
│  • Tool Registration                                     │
│  • Session Management                                    │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┬───────────────┐
        ▼                       ▼               ▼
┌───────────────┐    ┌──────────────────┐  ┌───────────┐
│ ArXiv Server  │    │ Wikipedia Server │  │ Filesystem│
│               │    │                  │  │  Server   │
│ • Search      │    │ • Search         │  │ • List    │
│ • Download    │    │ • Get Summary    │  │ • Read    │
│ • Get Info    │    │ • Download       │  │           │
└───────────────┘    └──────────────────┘  └───────────┘
```

## Directory Structure

```
mcp/
├── README.md                          # This file
├── servers/                           # MCP server implementations
│   ├── mcp_arxiv.py                  # ArXiv paper search/retrieval
│   ├── mcp_filesystem.py             # Sandboxed file system access
│   ├── mcp_wikipedia.py              # Wikipedia search/retrieval
│   └── mcp_server_template.py        # Template for custom servers
├── examples/                          # Integration examples
│   ├── genui_with_mcp.py             # GenUI + MCP integration
│   ├── mcp_client_example.py         # Basic MCP client usage
│   └── mcp_toolkit_demo.py           # Toolkit features demo
├── utils/                             # Helper utilities
│   └── mcp_helpers.py                # MCP setup utilities
├── storage/                           # Server data storage (gitignored)
│   ├── papers/                       # ArXiv papers
│   └── articles/                     # Wikipedia articles
├── context_docs/                      # Filesystem server context
└── run_mcp_servers.sh                # Server runner script
```

## Quick Start

### 1. Setup

The devcontainer automatically installs all dependencies. If running manually:

```bash
pip install -e ".[openai,mcp,mcp-proxy-gen]"
pip install arxiv wikipedia-api fastapi uvicorn nest-asyncio
```

### 2. Start MCP Servers

**Option A: Using the helper script (stdio mode)**
```bash
cd .devcontainer/generative-ui/mcp
bash run_mcp_servers.sh stdio
```

**Option B: Using the helper script (SSE mode)**
```bash
cd .devcontainer/generative-ui/mcp
bash run_mcp_servers.sh sse
```

**Option C: Start individual servers manually**
```bash
# ArXiv server (stdio)
python servers/mcp_arxiv.py stdio --storage-path ./storage/papers

# ArXiv server (SSE - HTTP on port 8000)
python servers/mcp_arxiv.py sse --storage-path ./storage/papers
```

### 3. Run Examples

```bash
# Basic MCP client example
python examples/mcp_client_example.py

# Toolkit demo
python examples/mcp_toolkit_demo.py

# Full GenUI integration (requires OpenAI API key)
export OPENAI_API_KEY="your-key-here"
python examples/genui_with_mcp.py
```

## Transport Modes

MCP supports two transport modes:

### stdio (Standard Input/Output)
- **Use for**: Local development, single-client scenarios
- **Pros**: Simple, no network setup required, secure
- **Cons**: One client per server instance
- **Example**:
  ```python
  from autogen.mcp.mcp_client import StdioConfig
  
  config = StdioConfig(
      server_name="arxiv",
      command="python",
      args=["servers/mcp_arxiv.py", "stdio", "--storage-path", "./papers"]
  )
  ```

### SSE (Server-Sent Events)
- **Use for**: Multi-client scenarios, remote access, debugging
- **Pros**: Multiple clients can connect, HTTP-based, easy to debug
- **Cons**: Requires port management, network configuration
- **Example**:
  ```python
  from autogen.mcp.mcp_client import SseConfig
  
  config = SseConfig(
      server_name="arxiv",
      url="http://localhost:8000"
  )
  ```

## Integration Patterns

### Pattern 1: Basic Tool Usage

```python
import asyncio
from pathlib import Path
from autogen.mcp import create_toolkit
from autogen.mcp.mcp_client import StdioConfig, MCPClientSessionManager

async def main():
    config = StdioConfig(
        server_name="arxiv",
        command="python",
        args=["servers/mcp_arxiv.py", "stdio", "--storage-path", "./papers"]
    )
    
    manager = MCPClientSessionManager()
    async with manager.open_session(config) as session:
        toolkit = await create_toolkit(session=session)
        
        # Call tools directly
        search_tool = next(t for t in toolkit.tools if t.name == "search_arxiv")
        results, _ = await search_tool.func_or_tool(query="machine learning", max_results=3)
        print(results)

asyncio.run(main())
```

### Pattern 2: Agent Integration

```python
from autogen.agentchat import AssistantAgent, UserProxyAgent

async def main():
    # ... setup session and toolkit as above ...
    
    assistant = AssistantAgent(
        name="research_agent",
        system_message="You are a research assistant.",
        llm_config={"model": "gpt-4o-mini"}
    )
    
    # Register toolkit with agent
    toolkit.register_for_llm(assistant)
    
    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    
    toolkit.register_for_execution(user_proxy)
    
    # Agent can now use MCP tools automatically
    await user_proxy.a_initiate_chat(
        assistant,
        message="Search for papers on 'neural networks'",
        max_turns=5
    )
```

### Pattern 3: Multiple Servers

```python
from autogen.tools import Toolkit

async def main():
    manager = MCPClientSessionManager()
    
    async with (
        manager.open_session(arxiv_config) as arxiv_session,
        manager.open_session(wiki_config) as wiki_session
    ):
        arxiv_toolkit = await create_toolkit(session=arxiv_session)
        wiki_toolkit = await create_toolkit(session=wiki_session)
        
        # Combine toolkits
        combined = Toolkit(tools=arxiv_toolkit.tools + wiki_toolkit.tools)
        
        # Register combined toolkit with agent
        combined.register_for_llm(assistant)
```

## Available MCP Servers

### ArXiv Server (`mcp_arxiv.py`)

Provides access to academic papers from arXiv.

**Tools**:
- `search_arxiv(query: str, max_results: int)` - Search for papers
- `download_paper(arxiv_id: str)` - Download paper PDF
- `get_paper_info(arxiv_id: str)` - Get paper metadata
- `list_papers()` - List downloaded papers

**Usage**:
```bash
python servers/mcp_arxiv.py stdio --storage-path ./papers
```

### Wikipedia Server (`mcp_wikipedia.py`)

Provides access to Wikipedia articles.

**Tools**:
- `search_wikipedia(query: str, max_results: int)` - Search for articles
- `download_article(title: str)` - Download article text
- `get_article_summary(title: str)` - Get article summary
- `list_articles()` - List downloaded articles

**Usage**:
```bash
python servers/mcp_wikipedia.py stdio --storage-path ./articles
```

### Filesystem Server (`mcp_filesystem.py`)

Provides sandboxed access to local files.

**Tools**:
- `list_files(relative_path: str)` - List directory contents
- `read_file(relative_path: str)` - Read file contents

**Security**: Access is restricted to the configured context path.

**Usage**:
```bash
python servers/mcp_filesystem.py stdio --context-path ./context_docs
```

## Creating Custom MCP Servers

Use the `mcp_server_template.py` as a starting point:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyCustomServer")

@mcp.tool()
def my_custom_tool(param: str) -> str:
    """Tool description that the LLM will see."""
    # Implement your tool logic
    return f"Result for {param}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("transport", choices=["stdio", "sse"])
    args = parser.parse_args()
    mcp.run(transport=args.transport)
```

### Best Practices for Custom Servers

1. **Clear Descriptions**: Write detailed docstrings - LLMs rely on these
2. **Type Hints**: Use proper type annotations for automatic schema generation
3. **Error Handling**: Return informative error messages, not exceptions
4. **Security**: Validate all inputs, especially for file/network operations
5. **Async Support**: Use `async def` for I/O-bound operations
6. **Configuration**: Use command-line args for paths, API keys, etc.

## Security Considerations

### Input Validation
- Always validate and sanitize user inputs
- Use type checking and schema validation
- Implement rate limiting for resource-intensive operations

### Sandboxing
- Filesystem server restricts access to configured context path
- Never allow arbitrary file system access
- Use separate storage directories for different security contexts

### API Keys
- Store API keys in environment variables, never in code
- Use secrets management for production deployments
- Rotate keys regularly and limit their scope

### Production Checklist
- [ ] Enable authentication for SSE servers
- [ ] Use HTTPS for network transport
- [ ] Implement request logging and monitoring
- [ ] Set resource limits (file sizes, request rates)
- [ ] Run servers with minimal OS privileges
- [ ] Audit custom server code for security issues

## Troubleshooting

### Server Won't Start
```bash
# Check if port is in use (for SSE mode)
lsof -i :8000

# Check server logs
python servers/mcp_arxiv.py stdio --storage-path ./papers 2>&1 | tee server.log
```

### Connection Issues
```python
# Verify server is responsive
import asyncio
from autogen.mcp.mcp_client import StdioConfig, MCPClientSessionManager

async def test_connection():
    config = StdioConfig(...)
    manager = MCPClientSessionManager()
    try:
        async with manager.open_session(config) as session:
            print("✓ Connected successfully")
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")

asyncio.run(test_connection())
```

### Tool Errors
- Check tool parameter types match the schema
- Verify file paths exist and are accessible
- Check API rate limits for external services
- Review server logs for detailed error messages

## Performance Tips

1. **Reuse Sessions**: Create one session and reuse it for multiple tool calls
2. **Parallel Calls**: Use `asyncio.gather()` for concurrent tool calls
3. **Caching**: Implement caching for frequently accessed data
4. **Resource Limits**: Set appropriate `max_results` parameters
5. **Connection Pooling**: For SSE mode, use connection pools

## Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io/introduction)
- [AG2 Documentation](https://docs.ag2.ai)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/fastmcp)
- [Example Notebooks](../../../notebook/mcp/)

## Contributing

To add new MCP servers or improve existing ones:

1. Use `mcp_server_template.py` as a starting point
2. Follow the coding standards in existing servers
3. Add comprehensive docstrings for all tools
4. Include usage examples in this README
5. Test with both stdio and SSE transports
6. Consider security implications of your tools

## Support

For issues or questions:
- Check existing examples in `examples/`
- Review the troubleshooting section above
- Consult AG2 documentation
- Open an issue on the AG2 GitHub repository
