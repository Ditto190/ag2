"""
MCP Toolkit Demo

This demo shows how to work with MCP toolkits in AG2,
including toolkit inspection, tool registration, and execution patterns.
"""

import asyncio
from pathlib import Path

from autogen.mcp import create_toolkit
from autogen.mcp.mcp_client import StdioConfig


async def inspect_toolkit():
    """
    Demonstrate toolkit inspection capabilities.
    Shows how to examine tools, their parameters, and schemas.
    """
    
    print("=" * 60)
    print("Toolkit Inspection Demo")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent.parent.parent.parent
    
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
        toolkit = await create_toolkit(session=session)
        
        print(f"\n📦 Toolkit contains {len(toolkit.tools)} tools\n")
        
        for tool in toolkit.tools:
            print("─" * 60)
            print(f"🔧 Tool: {tool.name}")
            print(f"   Description: {tool.description}")
            
            if hasattr(tool, "parameters_json_schema") and tool.parameters_json_schema:
                print(f"   Parameters:")
                schema = tool.parameters_json_schema
                if "properties" in schema:
                    for param_name, param_info in schema["properties"].items():
                        param_type = param_info.get("type", "any")
                        param_desc = param_info.get("description", "")
                        required = param_name in schema.get("required", [])
                        req_marker = "required" if required else "optional"
                        print(f"     • {param_name} ({param_type}) - {req_marker}")
                        if param_desc:
                            print(f"       {param_desc}")
            print()
        
        print("=" * 60)


async def toolkit_with_agent():
    """
    Demonstrate toolkit registration with an AG2 agent.
    Shows the complete integration pattern.
    """
    
    print("\n" + "=" * 60)
    print("Toolkit + Agent Integration Demo")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent.parent.parent.parent
    
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
    
    from autogen.agentchat import AssistantAgent, UserProxyAgent
    from autogen.mcp.mcp_client import MCPClientSessionManager
    
    manager = MCPClientSessionManager()
    
    async with manager.open_session(config) as session:
        toolkit = await create_toolkit(session=session)
        
        print(f"✓ Created toolkit with {len(toolkit.tools)} tools")
        
        # Create agent
        llm_config = {
            "model": "gpt-4o-mini",
            "api_type": "openai",
        }
        
        assistant = AssistantAgent(
            name="research_assistant",
            system_message="""You are a research assistant specialized in finding and
            analyzing academic papers. Use the available tools to search for papers
            and retrieve their information.""",
            llm_config=llm_config,
        )
        
        # Register toolkit with agent
        toolkit.register_for_llm(assistant)
        print("✓ Registered toolkit with LLM agent")
        
        # Create user proxy for tool execution
        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
        )
        
        toolkit.register_for_execution(user_proxy)
        print("✓ Registered toolkit with executor")
        
        print("\n" + "-" * 60)
        print("Starting chat with agent...")
        print("-" * 60 + "\n")
        
        # Initiate chat
        result = await user_proxy.a_initiate_chat(
            assistant,
            message="""Search arXiv for papers about 'transformers in NLP' (max 2 results).
            Then get detailed information about the first paper found.""",
            max_turns=4,
        )
        
        print("\n" + "=" * 60)
        print("Demo completed!")
        print("=" * 60)


async def multiple_toolkits_example():
    """
    Show how to work with multiple toolkits simultaneously.
    """
    
    print("\n" + "=" * 60)
    print("Multiple Toolkits Demo")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent.parent.parent.parent
    
    # Create two different server configs
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
    
    wiki_config = StdioConfig(
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
    from autogen.tools import Toolkit
    
    manager = MCPClientSessionManager()
    
    async with manager.open_session(arxiv_config) as arxiv_session, manager.open_session(
        wiki_config
    ) as wiki_session:
        # Create separate toolkits
        arxiv_toolkit = await create_toolkit(session=arxiv_session)
        wiki_toolkit = await create_toolkit(session=wiki_session)
        
        print(f"✓ ArXiv toolkit: {len(arxiv_toolkit.tools)} tools")
        print(f"✓ Wikipedia toolkit: {len(wiki_toolkit.tools)} tools")
        
        # Combine into a single toolkit
        combined = Toolkit(tools=arxiv_toolkit.tools + wiki_toolkit.tools)
        print(f"✓ Combined toolkit: {len(combined.tools)} tools")
        
        print("\nAvailable tools:")
        for tool in combined.tools:
            print(f"  • {tool.name}")
        
        print("\n" + "=" * 60)


async def tool_error_handling():
    """
    Demonstrate error handling when working with MCP tools.
    """
    
    print("\n" + "=" * 60)
    print("Tool Error Handling Demo")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent.parent.parent.parent
    
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
        toolkit = await create_toolkit(session=session)
        
        # Try calling a tool with invalid parameters
        info_tool = next((t for t in toolkit.tools if t.name == "get_paper_info"), None)
        if info_tool:
            print("\nTrying to get info for a non-existent paper...")
            try:
                result, _ = await info_tool.func_or_tool(arxiv_id="invalid-id-12345")
                print(f"Result: {result}")
            except Exception as e:
                print(f"❌ Caught error: {type(e).__name__}: {e}")
        
        print("\n" + "=" * 60)


async def main():
    """Run all toolkit demos."""
    
    print("\n" + "=" * 60)
    print("MCP Toolkit Demos")
    print("=" * 60 + "\n")
    
    try:
        # Run demos
        await inspect_toolkit()
        
        # Uncomment to run additional demos:
        # await toolkit_with_agent()
        # await multiple_toolkits_example()
        # await tool_error_handling()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
