#!/bin/bash
set -e

echo "==============================================="
echo "Setting up AG2 Generative UI with MCP"
echo "==============================================="

# Update pip
echo "Updating pip..."
pip install --upgrade pip

# Install AG2 with MCP and related extras
echo "Installing AG2 with MCP support..."
pip install -e ".[dev,openai,mcp,mcp-proxy-gen]"

# Install additional MCP dependencies
echo "Installing additional MCP dependencies..."
pip install arxiv wikipedia-api fastapi uvicorn nest-asyncio

# Create MCP storage directories
echo "Creating MCP storage directories..."
mkdir -p .devcontainer/generative-ui/mcp/storage/papers
mkdir -p .devcontainer/generative-ui/mcp/storage/articles
mkdir -p .devcontainer/generative-ui/mcp/context_docs

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Install Claude Code CLI (optional)
echo "Installing Claude Code CLI..."
npm install --location=global @anthropic-ai/claude-code || echo "Claude Code CLI installation skipped"

echo "==============================================="
echo "Setup complete!"
echo "==============================================="
echo ""
echo "MCP servers available:"
echo "  - ArXiv: python .devcontainer/generative-ui/mcp/servers/mcp_arxiv.py"
echo "  - Filesystem: python .devcontainer/generative-ui/mcp/servers/mcp_filesystem.py"
echo "  - Wikipedia: python .devcontainer/generative-ui/mcp/servers/mcp_wikipedia.py"
echo ""
echo "Quick start:"
echo "  cd .devcontainer/generative-ui/mcp"
echo "  bash run_mcp_servers.sh"
echo ""
