#!/bin/bash

echo "Setting up AG2 Generative UI development environment..."

# Install AG2 with all necessary dependencies
echo "Installing AG2..."
pip install -e .[openai,anthropic,gemini,together] --quiet

# Install additional Python dependencies for web development
echo "Installing Python web development dependencies..."
pip install fastapi uvicorn[standard] pydantic websockets --quiet

# Install Node.js dependencies globally
echo "Installing global npm packages..."
npm install -g pnpm typescript tsx --silent

echo "Setup complete! 🎉"
echo ""
echo "To get started with Generative UI development:"
echo "  1. Navigate to the templates/generative-ui directory"
echo "  2. Follow the README instructions to set up your first app"
echo ""
