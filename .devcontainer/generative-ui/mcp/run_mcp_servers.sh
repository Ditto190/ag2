#!/bin/bash

# MCP Server Runner Script
# Starts common MCP servers for development

set -e

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVERS_DIR="$SCRIPT_DIR/servers"
STORAGE_DIR="$SCRIPT_DIR/storage"

# Create storage directories if they don't exist
mkdir -p "$STORAGE_DIR/papers"
mkdir -p "$STORAGE_DIR/articles"
mkdir -p "$SCRIPT_DIR/context_docs"

echo "==============================================="
echo "Starting MCP Servers"
echo "==============================================="
echo ""
echo "Storage paths:"
echo "  Papers: $STORAGE_DIR/papers"
echo "  Articles: $STORAGE_DIR/articles"
echo "  Context docs: $SCRIPT_DIR/context_docs"
echo ""

# Check if running in SSE mode (default) or stdio mode
MODE="${1:-stdio}"

if [ "$MODE" = "sse" ]; then
    echo "Starting servers in SSE mode (HTTP)..."
    echo ""

    # Start ArXiv server on port 8000
    echo "Starting MCP ArXiv server on port 8000..."
    python "$SERVERS_DIR/mcp_arxiv.py" sse --storage-path "$STORAGE_DIR/papers" &
    ARXIV_PID=$!

    # Start Filesystem server on port 8001
    echo "Starting MCP Filesystem server on port 8001..."
    python "$SERVERS_DIR/mcp_filesystem.py" sse --context-path "$SCRIPT_DIR/context_docs" &
    FILESYSTEM_PID=$!

    # Start Wikipedia server on port 8002
    echo "Starting MCP Wikipedia server on port 8002..."
    python "$SERVERS_DIR/mcp_wikipedia.py" sse --storage-path "$STORAGE_DIR/articles" &
    WIKIPEDIA_PID=$!

    echo ""
    echo "==============================================="
    echo "MCP servers running in background:"
    echo "  ArXiv (PID: $ARXIV_PID) - http://localhost:8000"
    echo "  Filesystem (PID: $FILESYSTEM_PID) - http://localhost:8001"
    echo "  Wikipedia (PID: $WIKIPEDIA_PID) - http://localhost:8002"
    echo "==============================================="
    echo ""
    echo "To stop servers, run:"
    echo "  kill $ARXIV_PID $FILESYSTEM_PID $WIKIPEDIA_PID"
    echo ""

    # Save PIDs to file for easy cleanup
    echo "$ARXIV_PID $FILESYSTEM_PID $WIKIPEDIA_PID" > "$SCRIPT_DIR/.mcp_server_pids"
    echo "PIDs saved to $SCRIPT_DIR/.mcp_server_pids"

elif [ "$MODE" = "stdio" ]; then
    echo "Servers configured for stdio mode."
    echo "Use them in your client code with StdioConfig."
    echo ""
    echo "Example:"
    echo "  from autogen.mcp.mcp_client import StdioConfig"
    echo "  config = StdioConfig("
    echo "      server_name='arxiv',"
    echo "      command='python',"
    echo "      args=['$SERVERS_DIR/mcp_arxiv.py', 'stdio', '--storage-path', '$STORAGE_DIR/papers']"
    echo "  )"
    echo ""
else
    echo "Unknown mode: $MODE"
    echo "Usage: $0 [sse|stdio]"
    exit 1
fi
