"""
MCP Helper Utilities

This module provides utility functions for setting up and managing MCP connections
in AG2 Generative UI applications.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from autogen.mcp.mcp_client import MCPClientSessionManager, SseConfig, StdioConfig
from mcp.client.session import ClientSession


async def create_stdio_session(
    server_name: str,
    command: str,
    args: list[str],
    environment: dict[str, str] | None = None,
    working_dir: str | Path | None = None,
) -> tuple[MCPClientSessionManager, ClientSession]:
    """
    Create an MCP client session using stdio transport.
    
    Args:
        server_name: Name identifier for the MCP server
        command: Command to execute (e.g., "python")
        args: List of arguments for the command
        environment: Optional environment variables
        working_dir: Optional working directory for the server process
        
    Returns:
        Tuple of (session_manager, session)
        
    Example:
        >>> manager, session = await create_stdio_session(
        ...     server_name="arxiv",
        ...     command="python",
        ...     args=["mcp/servers/mcp_arxiv.py", "stdio", "--storage-path", "./papers"]
        ... )
    """
    config = StdioConfig(
        server_name=server_name,
        command=command,
        args=args,
        environment=environment,
        working_dir=working_dir,
    )
    
    manager = MCPClientSessionManager()
    session = None
    
    async with manager.open_session(config) as sess:
        session = sess
        return manager, session


async def create_sse_session(
    server_name: str,
    url: str,
    headers: dict | None = None,
    timeout: float = 5.0,
) -> tuple[MCPClientSessionManager, ClientSession]:
    """
    Create an MCP client session using SSE (Server-Sent Events) transport.
    
    Args:
        server_name: Name identifier for the MCP server
        url: URL of the SSE server endpoint
        headers: Optional HTTP headers to send
        timeout: HTTP request timeout in seconds
        
    Returns:
        Tuple of (session_manager, session)
        
    Example:
        >>> manager, session = await create_sse_session(
        ...     server_name="arxiv",
        ...     url="http://localhost:8000"
        ... )
    """
    config = SseConfig(
        server_name=server_name,
        url=url,
        headers=headers,
        timeout=timeout,
    )
    
    manager = MCPClientSessionManager()
    session = None
    
    async with manager.open_session(config) as sess:
        session = sess
        return manager, session


@asynccontextmanager
async def mcp_toolkit_context(
    server_name: str,
    command: str,
    args: list[str],
    use_mcp_tools: bool = True,
    use_mcp_resources: bool = True,
    resource_download_folder: Path | str | None = None,
) -> AsyncIterator[tuple[ClientSession, "Toolkit"]]:  # type: ignore
    """
    Context manager that creates an MCP session and toolkit, automatically cleaning up.
    
    Args:
        server_name: Name identifier for the MCP server
        command: Command to execute
        args: List of arguments for the command
        use_mcp_tools: Whether to include MCP tools in the toolkit
        use_mcp_resources: Whether to include MCP resources in the toolkit
        resource_download_folder: Optional folder for downloading resources
        
    Yields:
        Tuple of (session, toolkit)
        
    Example:
        >>> async with mcp_toolkit_context(
        ...     server_name="arxiv",
        ...     command="python",
        ...     args=["mcp/servers/mcp_arxiv.py", "stdio", "--storage-path", "./papers"]
        ... ) as (session, toolkit):
        ...     # Use the toolkit with your agent
        ...     toolkit.register_for_llm(agent)
    """
    from autogen.mcp import create_toolkit
    
    config = StdioConfig(
        server_name=server_name,
        command=command,
        args=args,
    )
    
    manager = MCPClientSessionManager()
    
    async with manager.open_session(config) as session:
        toolkit = await create_toolkit(
            session=session,
            use_mcp_tools=use_mcp_tools,
            use_mcp_resources=use_mcp_resources,
            resource_download_folder=resource_download_folder,
        )
        yield session, toolkit


def get_default_mcp_config(server_type: str, base_path: Path | None = None) -> dict:
    """
    Get default configuration for common MCP servers.
    
    Args:
        server_type: Type of server ("arxiv", "filesystem", "wikipedia")
        base_path: Base path for storage/context directories
        
    Returns:
        Dictionary with server configuration
        
    Example:
        >>> config = get_default_mcp_config("arxiv", Path("/workspace"))
        >>> print(config)
        {'command': 'python', 'args': [...], 'server_name': 'arxiv'}
    """
    if base_path is None:
        base_path = Path.cwd()
    
    configs = {
        "arxiv": {
            "server_name": "arxiv",
            "command": "python",
            "args": [
                str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_arxiv.py"),
                "stdio",
                "--storage-path",
                str(base_path / ".devcontainer/generative-ui/mcp/storage/papers"),
            ],
        },
        "filesystem": {
            "server_name": "filesystem",
            "command": "python",
            "args": [
                str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_filesystem.py"),
                "stdio",
                "--context-path",
                str(base_path / ".devcontainer/generative-ui/mcp/context_docs"),
            ],
        },
        "wikipedia": {
            "server_name": "wikipedia",
            "command": "python",
            "args": [
                str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_wikipedia.py"),
                "stdio",
                "--storage-path",
                str(base_path / ".devcontainer/generative-ui/mcp/storage/articles"),
            ],
        },
    }
    
    if server_type not in configs:
        raise ValueError(f"Unknown server type: {server_type}. Available: {list(configs.keys())}")
    
    return configs[server_type]
