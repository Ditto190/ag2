"""
Generative UI with MCP Integration Example

This example demonstrates how to integrate MCP servers with AG2 agents
for building Generative UI applications with real-time data retrieval.

The pattern shown here enables:
1. Tool orchestration for GenUI via MCP protocol
2. External data retrieval and grounding for generated UIs
3. Standardized agent-to-service communication
"""

import asyncio
from pathlib import Path

from autogen.agentchat import AssistantAgent, UserProxyAgent
from autogen.mcp import create_toolkit
from autogen.mcp.mcp_client import StdioConfig


async def setup_mcp_genui_agent():
    """
    Set up an MCP-enabled AG2 agent for Generative UI applications.

    This function demonstrates:
    - Connecting to an MCP server (ArXiv in this case)
    - Creating a toolkit from MCP tools
    - Registering tools with an AG2 agent
    - Using the agent to retrieve and process data for UI generation
    """

    # Get the base path
    base_path = Path(__file__).parent.parent.parent.parent.parent

    # Configure the MCP server connection (stdio transport for local development)
    server_params = StdioConfig(
        server_name="arxiv",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_arxiv.py"),
            "stdio",
            "--storage-path",
            str(base_path / ".devcontainer/generative-ui/mcp/storage/papers"),
        ],
    )

    print("=" * 60)
    print("Starting MCP ArXiv Server Connection...")
    print("=" * 60)

    # Create session manager and open session
    from autogen.mcp.mcp_client import MCPClientSessionManager

    manager = MCPClientSessionManager()

    async with manager.open_session(server_params) as session:
        print("✓ Connected to MCP ArXiv server")

        # Create toolkit from MCP tools
        toolkit = await create_toolkit(
            session=session,
            use_mcp_tools=True,
            use_mcp_resources=False,
        )

        print(f"✓ Created toolkit with {len(toolkit.tools)} tools")
        for tool in toolkit.tools:
            print(f"  - {tool.name}: {tool.description}")

        # Configure LLM (using OpenAI GPT-4 as example)
        llm_config = {
            "model": "gpt-4o-mini",
            "api_type": "openai",
        }

        # Create an agent with MCP tools
        genui_agent = AssistantAgent(
            name="genui_agent",
            system_message="""You are a Generative UI agent that creates interactive user interfaces
            grounded in real data. When asked to create a UI, always:
            1. First retrieve relevant data using available tools
            2. Analyze and structure the data
            3. Describe the UI components and data flow
            4. Provide the grounded data that would populate the UI

            Focus on data-driven, factual UI generation.""",
            llm_config=llm_config,
        )

        # Register MCP tools with the agent
        toolkit.register_for_llm(genui_agent)

        # Create a user proxy for interaction
        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
        )

        toolkit.register_for_execution(user_proxy)

        print("\n" + "=" * 60)
        print("Example 1: Search and retrieve paper data")
        print("=" * 60)

        # Example task: Search for papers and create a paper browser UI concept
        result = await user_proxy.a_initiate_chat(
            genui_agent,
            message="""Search arXiv for recent papers on 'large language models' (max 3 results).
            Then get detailed information for the first paper found.
            Finally, describe a UI component design that would display this paper data effectively.""",
            max_turns=5,
        )

        print("\n" + "=" * 60)
        print("Chat completed!")
        print("=" * 60)

        return result


async def multi_server_example():
    """
    Example demonstrating how to use multiple MCP servers simultaneously.

    This shows how to combine data from different sources (ArXiv + Wikipedia)
    to create rich, multi-faceted UIs.
    """

    base_path = Path(__file__).parent.parent.parent.parent.parent

    # Configure multiple MCP servers
    arxiv_config = StdioConfig(
        server_name="arxiv",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_arxiv.py"),
            "stdio",
            "--storage-path",
            str(base_path / ".devcontainer/generative-ui/mcp/storage/papers"),
        ],
    )

    wikipedia_config = StdioConfig(
        server_name="wikipedia",
        command="python",
        args=[
            str(base_path / ".devcontainer/generative-ui/mcp/servers/mcp_wikipedia.py"),
            "stdio",
            "--storage-path",
            str(base_path / ".devcontainer/generative-ui/mcp/storage/articles"),
        ],
    )

    print("=" * 60)
    print("Multi-Server Example: ArXiv + Wikipedia")
    print("=" * 60)

    from autogen.mcp.mcp_client import MCPClientSessionManager

    manager = MCPClientSessionManager()

    # Open both sessions
    async with manager.open_session(arxiv_config) as arxiv_session, manager.open_session(
        wikipedia_config
    ) as wiki_session:
        print("✓ Connected to MCP servers")

        # Create toolkits from both sessions
        arxiv_toolkit = await create_toolkit(session=arxiv_session)
        wiki_toolkit = await create_toolkit(session=wiki_session)

        print(f"✓ ArXiv toolkit: {len(arxiv_toolkit.tools)} tools")
        print(f"✓ Wikipedia toolkit: {len(wiki_toolkit.tools)} tools")

        # Combine tools from both toolkits
        from autogen.tools import Toolkit

        combined_toolkit = Toolkit(tools=arxiv_toolkit.tools + wiki_toolkit.tools)

        print(f"✓ Combined toolkit: {len(combined_toolkit.tools)} tools")

        # Create agent with combined tools
        llm_config = {
            "model": "gpt-4o-mini",
            "api_type": "openai",
        }

        research_agent = AssistantAgent(
            name="research_agent",
            system_message="""You are a research assistant that combines academic and encyclopedic knowledge.
            Use arXiv for papers and Wikipedia for background information.
            Always cite your sources and provide comprehensive, factual information.""",
            llm_config=llm_config,
        )

        combined_toolkit.register_for_llm(research_agent)

        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
        )

        combined_toolkit.register_for_execution(user_proxy)

        print("\n" + "=" * 60)
        print("Example: Research task combining multiple sources")
        print("=" * 60)

        result = await user_proxy.a_initiate_chat(
            research_agent,
            message="""Research the topic 'neural networks':
            1. Search Wikipedia for a general overview
            2. Search arXiv for recent research papers
            3. Describe how you would design a learning dashboard UI that presents both
               the foundational concepts (from Wikipedia) and cutting-edge research (from arXiv)""",
            max_turns=8,
        )

        return result


async def filesystem_context_example():
    """
    Example showing how to use the filesystem MCP server to ground UI generation
    in existing documentation or content files.
    """

    base_path = Path(__file__).parent.parent.parent.parent.parent
    context_path = base_path / ".devcontainer/generative-ui/mcp/context_docs"

    # Create a sample context document
    context_path.mkdir(parents=True, exist_ok=True)
    sample_doc = context_path / "ui_guidelines.txt"
    sample_doc.write_text(
        """UI Design Guidelines for GenUI Applications

1. Accessibility First
   - Ensure all components have proper ARIA labels
   - Maintain color contrast ratios of at least 4.5:1
   - Support keyboard navigation

2. Data Visualization
   - Use charts for numeric data trends
   - Provide table views for detailed data inspection
   - Include export functionality for datasets

3. Progressive Disclosure
   - Show summaries first, details on demand
   - Use expandable sections for lengthy content
   - Implement pagination for large datasets

4. Real-time Updates
   - Indicate loading states clearly
   - Show timestamps for data freshness
   - Provide refresh/reload options
"""
    )

    print("✓ Created sample context document")

    filesystem_config = StdioConfig(
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

    async with manager.open_session(filesystem_config) as session:
        toolkit = await create_toolkit(session=session)

        llm_config = {
            "model": "gpt-4o-mini",
            "api_type": "openai",
        }

        ui_designer = AssistantAgent(
            name="ui_designer",
            system_message="""You are a UI/UX designer that follows documented guidelines.
            Always check for guidelines in the context documents before designing.
            Cite specific guidelines you're following in your designs.""",
            llm_config=llm_config,
        )

        toolkit.register_for_llm(ui_designer)

        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
        )

        toolkit.register_for_execution(user_proxy)

        print("\n" + "=" * 60)
        print("Example: Guideline-driven UI design")
        print("=" * 60)

        result = await user_proxy.a_initiate_chat(
            ui_designer,
            message="""First, read the UI guidelines document.
            Then design a data dashboard UI for displaying research papers,
            ensuring you follow all the guidelines you found.""",
            max_turns=5,
        )

        return result


async def main():
    """Run all examples."""

    print("\n" + "=" * 60)
    print("AG2 Generative UI with MCP Integration Examples")
    print("=" * 60 + "\n")

    try:
        # Run the basic example
        print("\n### Running Basic MCP Integration Example ###\n")
        await setup_mcp_genui_agent()

        print("\n\n### Running Multi-Server Example ###\n")
        # Uncomment to run:
        # await multi_server_example()

        print("\n\n### Running Filesystem Context Example ###\n")
        # Uncomment to run:
        # await filesystem_context_example()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Note: This example requires:
    # 1. OpenAI API key set in environment (OPENAI_API_KEY)
    # 2. MCP servers to be available
    # 3. AG2 with MCP extras installed

    asyncio.run(main())
