# AG2 Templates

This directory contains ready-to-use templates for building applications with AG2.

## Available Templates

### 🎨 Generative UI Template

**Location:** `templates/generative-ui/`

A production-ready template for building **Generative UI applications** where AI agents dynamically generate and stream user interface components based on user interactions and context.

**What's Included:**
- Full-stack boilerplate (FastAPI + Next.js)
- Multi-agent orchestration system
- Dynamic UI component generation
- WebSocket support for real-time streaming
- Type-safe communication (Pydantic + TypeScript)
- Pre-built components (Cards, Tables, Alerts)
- Comprehensive documentation and examples

**Quick Start:**
```bash
cd templates/generative-ui
# Follow the GETTING_STARTED.md guide
```

**Use Cases:**
- Conversational dashboards
- Interactive data analysis tools
- Dynamic form generation
- AI-powered research interfaces
- Content creation tools

**Documentation:**
- [Getting Started Guide](generative-ui/GETTING_STARTED.md) - Quick introduction
- [Full README](generative-ui/README.md) - Comprehensive documentation
- [Quick Start](generative-ui/QUICKSTART.md) - Detailed setup instructions
- [Examples](generative-ui/examples/README.md) - Real-world use cases

**GitHub Codespaces:**

Use the dedicated **"AG2 Generative UI Development"** devcontainer:
1. Click the "Code" button on GitHub
2. Select "Codespaces" tab
3. Choose "New codespace"
4. Select the "generative-ui" devcontainer configuration

The devcontainer includes:
- Python 3.11 with AG2 and all dependencies
- Node.js 20 for frontend development
- Pre-configured VS Code extensions
- Automatic port forwarding (3000, 8000)

---

## Creating Your Own Template

Want to create a template for a specific use case? Here's how:

1. **Create the template directory:**
   ```bash
   mkdir -p templates/my-template
   ```

2. **Add essential files:**
   - `README.md` - Overview and features
   - `GETTING_STARTED.md` - Quick start guide
   - Example code and boilerplate
   - Configuration files

3. **Optional: Create a devcontainer:**
   ```bash
   mkdir -p .devcontainer/my-template
   # Add devcontainer.json and setup.sh
   ```

4. **Document your template:**
   - Clear use case description
   - Setup instructions
   - Example usage
   - Troubleshooting tips

5. **Submit a PR:**
   - Follow [CONTRIBUTING.md](../CONTRIBUTING.md)
   - Include working examples
   - Add tests if applicable

## Template Guidelines

Good templates should:

- ✅ Solve a specific, common use case
- ✅ Include working example code
- ✅ Have clear documentation
- ✅ Follow AG2 best practices
- ✅ Be production-ready (or clearly marked as experimental)
- ✅ Include proper error handling
- ✅ Have type safety (TypeScript, Pydantic, etc.)

## Resources

- [AG2 Documentation](https://docs.ag2.ai/)
- [AG2 Examples Repository](https://github.com/ag2ai/build-with-ag2)
- [AG2 Discord Community](https://discord.gg/pAbnFJrkgZ)

## Contributing

We welcome new templates! If you've built something useful with AG2, consider sharing it:

1. Create your template following the guidelines above
2. Test it thoroughly
3. Submit a pull request
4. Join the discussion on Discord

---

**Need Help?**

- 💬 [Discord Community](https://discord.gg/pAbnFJrkgZ)
- 📖 [Documentation](https://docs.ag2.ai/)
- 🐛 [GitHub Issues](https://github.com/ag2ai/ag2/issues)
