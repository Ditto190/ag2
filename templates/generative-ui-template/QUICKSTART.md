# Quick Start Guide

## Get Started in 5 Minutes

### 1. Clone or Copy the Template

```bash
# If using from the AG2 repository
cd templates/generative-ui-template

# Or copy the entire directory to your project location
cp -r templates/generative-ui-template /path/to/your/project
cd /path/to/your/project
```

### 2. Set Up Environment

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

Create an `OAI_CONFIG_LIST` file in the root directory:

```json
[
  {
    "model": "gpt-4",
    "api_key": "sk-your-openai-api-key-here"
  }
]
```

Or set environment variables:

```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

### 4. Run the Application

```bash
python backend/main.py
```

The application will start at `http://localhost:8000`

### 5. Try It Out!

Open your browser and navigate to:
- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

Try these example prompts:
- "Create a user registration form"
- "Show me a dashboard with analytics"
- "Display a table of user data"
- "Create a chat interface"

## Next Steps

### Customize Your Agents

Edit `backend/agents.py` to modify agent behavior:
- Change system messages
- Add new agents
- Adjust temperatures and parameters

### Add Custom Tools

Edit `backend/tools.py` to add new capabilities:
- Data source connections
- Custom UI components
- Business logic

### Modify UI Templates

Update templates in `frontend/templates/`:
- Customize styling in `frontend/static/css/styles.css`
- Add new components in `frontend/static/js/app.js`

### Deploy

Deploy to your favorite platform:
- **Docker**: Build with `docker build -t generative-ui .`
- **Cloud**: Deploy to Azure, AWS, GCP, or Vercel
- **Local**: Run with systemd or supervisor

## Troubleshooting

### No API Key Error
Make sure you've set up your OpenAI API key in either:
- `OAI_CONFIG_LIST` file, or
- `OPENAI_API_KEY` environment variable

### Port Already in Use
Change the port in `.env`:
```
PORT=8001
```

### Module Not Found
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Learn More

- [AG2 Documentation](https://docs.ag2.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AG2 Examples](https://github.com/ag2ai/build-with-ag2)

## Support

For help:
- Check the [AG2 Discord](https://discord.gg/pAbnFJrkgZ)
- Review [AG2 Documentation](https://docs.ag2.ai/)
- Open an issue on GitHub
