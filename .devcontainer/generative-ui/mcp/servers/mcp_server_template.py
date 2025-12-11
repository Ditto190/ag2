"""
MCP Server Template

This template provides a starting point for creating custom MCP servers
that can be integrated with AG2 agents for Generative UI applications.

Example usage:
    python mcp_server_template.py stdio --config-param value
    python mcp_server_template.py sse --config-param value
"""

import argparse
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with a descriptive name
mcp = FastMCP("TemplateServer")

# Parse configuration arguments
parser = argparse.ArgumentParser(description="Template MCP Server")
parser.add_argument("--config-path", required=False, help="Path to configuration file")
args, unknown = parser.parse_known_args()

# Initialize server configuration
CONFIG_PATH = Path(args.config_path).resolve() if args.config_path else None


@mcp.tool()
def example_tool(query: str, max_results: int = 5) -> list[str]:
    """
    Example tool that demonstrates basic MCP tool structure.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        List of result strings
    """
    # Implement your tool logic here
    results = [f"Result {i+1} for query '{query}'" for i in range(max_results)]
    return results


@mcp.tool()
def example_data_retrieval(item_id: str) -> dict[str, str]:
    """
    Example tool for retrieving structured data.

    Args:
        item_id: The unique identifier for the item to retrieve

    Returns:
        Dictionary containing item data
    """
    # Implement your data retrieval logic here
    return {
        "id": item_id,
        "title": f"Item {item_id}",
        "description": "This is example data",
        "status": "active",
    }


@mcp.tool()
def example_action(action_type: str, parameters: dict) -> str:
    """
    Example tool for performing actions.

    Args:
        action_type: Type of action to perform
        parameters: Action-specific parameters as a dictionary

    Returns:
        Status message indicating action result
    """
    # Implement your action logic here
    return f"Action '{action_type}' completed with parameters: {parameters}"


# Tips for creating effective MCP tools:
#
# 1. Clear Descriptions: Provide detailed docstrings that explain what the tool does,
#    its parameters, and return values. LLMs use these for understanding tool capabilities.
#
# 2. Type Annotations: Use proper type hints (str, int, dict, list, etc.) to help
#    validate inputs and generate accurate schemas.
#
# 3. Error Handling: Consider adding try-except blocks for robust error handling.
#    Return informative error messages instead of raising exceptions when appropriate.
#
# 4. Async Support: For I/O-bound operations, consider using async def to improve
#    performance when handling multiple concurrent requests.
#
# 5. Security: Always validate and sanitize inputs, especially when dealing with
#    file system operations, API calls, or user data.
#
# 6. Configuration: Use command-line arguments or environment variables for
#    server-specific configuration (API keys, paths, etc.).


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Template MCP Server")
    parser.add_argument(
        "transport",
        choices=["stdio", "sse", "streamable-http"],
        help="Transport mode (stdio for local, sse for network)",
    )
    parser.add_argument(
        "--config-path",
        required=False,
        help="Path to configuration file or directory",
    )
    args = parser.parse_args()

    # Run the server with the specified transport
    mcp.run(transport=args.transport)
