"""
Simple MCP Client Example

This script demonstrates basic MCP client usage patterns with AG2.
Based on the mcp_client.ipynb notebook examples.
"""

import asyncio
from pathlib import Path

from autogen.mcp import create_toolkit
from autogen.mcp.mcp_client import StdioConfig


async def basic_toolkit_example():
    """
    Basic example of creating and using an MCP toolkit.

    This demonstrates:
    1. Configuring an MCP server connection
    2. Creating a toolkit
    3. Inspecting available tools
    4. Calling tools directly
    """

    print("=" * 60)
    print("Basic MCP Toolkit Example")
    print("=" * 60)

    # Get paths
    base_path = Path(__file__).parent.parent.parent.parent.parent

    # Configure ArXiv server
    config = StdioConfig(
        server_name="arxiv",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_arxiv.py"),
            "stdio",
            "--storage-path",
            str(base_path / ".devcontainer/generative-ui/mcp/storage/papers"),
        ],
    )

    from autogen.mcp.mcp_client import MCPClientSessionManager

    manager = MCPClientSessionManager()

    async with manager.open_session(config) as session:
        print("✓ Connected to MCP server")

        # Create toolkit
        toolkit = await create_toolkit(session=session)

        print(f"\n✓ Toolkit created with {len(toolkit.tools)} tools:\n")
        for tool in toolkit.tools:
            print(f"  📦 {tool.name}")
            print(f"     {tool.description}")
            print()

        # Example: Call a tool directly
        print("-" * 60)
        print("Calling search_arxiv tool...")
        print("-" * 60)

        search_tool = next((t for t in toolkit.tools if t.name == "search_arxiv"), None)
        if search_tool:
            result, _ = await search_tool.func_or_tool(query="quantum computing", max_results=2)
            print(f"\nSearch results: {result}")

            if isinstance(result, list) and result:
                # Get info about the first paper
                info_tool = next((t for t in toolkit.tools if t.name == "get_paper_info"), None)
                if info_tool:
                    print("\n" + "-" * 60)
                    print("Getting paper info...")
                    print("-" * 60)
                    paper_info, _ = await info_tool.func_or_tool(arxiv_id=result[0])
                    print(f"\nPaper info: {paper_info}")

        print("\n" + "=" * 60)
        print("Example completed!")
        print("=" * 60)


async def wikipedia_example():
    """
    Example using the Wikipedia MCP server.
    """

    print("\n" + "=" * 60)
    print("Wikipedia MCP Example")
    print("=" * 60)

    base_path = Path(__file__).parent.parent.parent.parent.parent

    config = StdioConfig(
        server_name="wikipedia",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_wikipedia.py"),
            "stdio",
            "--storage-path",
            str(base_path / ".devcontainer/generative-ui/mcp/storage/articles"),
        ],
    )

    from autogen.mcp.mcp_client import MCPClientSessionManager

    manager = MCPClientSessionManager()

    async with manager.open_session(config) as session:
        print("✓ Connected to Wikipedia MCP server")

        toolkit = await create_toolkit(session=session)

        print(f"✓ Available tools: {[t.name for t in toolkit.tools]}\n")

        # Search Wikipedia
        search_tool = next((t for t in toolkit.tools if t.name == "search_wikipedia"), None)
        if search_tool:
            print("-" * 60)
            print("Searching Wikipedia for 'Machine Learning'...")
            print("-" * 60)

            results, _ = await search_tool.func_or_tool(query="Machine Learning", max_results=3)
            print(f"\nSearch results: {results}")

            if isinstance(results, list) and results:
                # Get summary of first result
                summary_tool = next((t for t in toolkit.tools if t.name == "get_article_summary"), None)
                if summary_tool:
                    print("\n" + "-" * 60)
                    print(f"Getting summary for '{results[0]}'...")
                    print("-" * 60)

                    summary, _ = await summary_tool.func_or_tool(title=results[0])
                    print(f"\nSummary: {summary}")

        print("\n" + "=" * 60)
        print("Wikipedia example completed!")
        print("=" * 60)


async def filesystem_example():
    """
    Example using the Filesystem MCP server.
    """

    print("\n" + "=" * 60)
    print("Filesystem MCP Example")
    print("=" * 60)

    base_path = Path(__file__).parent.parent.parent.parent.parent
    context_path = base_path / ".devcontainer/generative-ui/mcp/context_docs"

    # Ensure context directory exists and has a sample file
    context_path.mkdir(parents=True, exist_ok=True)
    sample_file = context_path / "sample.txt"
    sample_file.write_text("This is a sample document for MCP filesystem demo.\nLine 2 of the sample.")

    config = StdioConfig(
        server_name="filesystem",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_filesystem.py"),
            "stdio",
            "--context-path",
            str(context_path),
        ],
    )

    from autogen.mcp.mcp_client import MCPClientSessionManager

    manager = MCPClientSessionManager()

    async with manager.open_session(config) as session:
        print("✓ Connected to Filesystem MCP server")

        toolkit = await create_toolkit(session=session)

        print(f"✓ Available tools: {[t.name for t in toolkit.tools]}\n")

        # List files
        list_tool = next((t for t in toolkit.tools if t.name == "list_files"), None)
        if list_tool:
            print("-" * 60)
            print("Listing files in context directory...")
            print("-" * 60)

            files, _ = await list_tool.func_or_tool(relative_path="")
            print(f"\nFiles: {files}")

            # Read a file
            if isinstance(files, list) and "sample.txt" in files:
                read_tool = next((t for t in toolkit.tools if t.name == "read_file"), None)
                if read_tool:
                    print("\n" + "-" * 60)
                    print("Reading sample.txt...")
                    print("-" * 60)

                    content, _ = await read_tool.func_or_tool(relative_path="sample.txt")
                    print(f"\nContent:\n{content}")

        print("\n" + "=" * 60)
        print("Filesystem example completed!")
        print("=" * 60)


async def main():
    """Run all examples."""

    print("\n" + "=" * 60)
    print("MCP Client Examples")
    print("=" * 60 + "\n")

    try:
        # Run examples
        await basic_toolkit_example()

        # Uncomment to run additional examples:
        # await wikipedia_example()
        # await filesystem_example()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
