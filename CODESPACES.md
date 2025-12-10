# Using the AG2 Generative UI Template in GitHub Codespaces

This guide explains how to use the Generative UI template in GitHub Codespaces.

## What is GitHub Codespaces?

GitHub Codespaces provides a complete development environment in the cloud, accessible from your browser. It comes pre-configured with all the tools and dependencies you need.

## Option 1: Quick Start with Codespaces (Recommended)

### Step 1: Create a Codespace

1. Navigate to the AG2 repository on GitHub
2. Click the **"Code"** button (green button)
3. Select the **"Codespaces"** tab
4. Click **"Create codespace on [branch-name]"**

### Step 2: Select the Generative UI Configuration

When creating the codespace, you can select different devcontainer configurations:

- Choose **"AG2 Generative UI Development"** from the configuration dropdown
- Or create with the default and manually select it later

### Step 3: Wait for Setup

The codespace will automatically:
- Install Python 3.11 and all AG2 dependencies
- Install Node.js 20 and frontend tools
- Set up VS Code with recommended extensions
- Forward ports 3000 and 8000

This takes about 2-3 minutes on first launch.

### Step 4: Configure Your API Keys

Once the codespace is ready:

```bash
# Navigate to the template
cd templates/generative-ui

# Set up backend environment
cd backend
cp .env.example .env

# Edit .env and add your OpenAI API key
# You can use the VS Code editor or command line:
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Set up frontend environment
cd ../frontend
cp .env.example .env.local
```

### Step 5: Start the Application

Open two terminals in VS Code:

**Terminal 1 (Backend):**
```bash
cd templates/generative-ui/backend
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd templates/generative-ui/frontend
pnpm install  # First time only
pnpm dev
```

### Step 6: Open the Application

When the frontend starts, VS Code will show a notification:
- Click **"Open in Browser"** or
- Go to the **"Ports"** tab and click the globe icon next to port 3000

## Option 2: Use an Existing Codespace

If you already have a codespace:

1. Open the codespace
2. Navigate to `templates/generative-ui`
3. Follow steps 4-6 from Option 1

## Using Codespace Secrets for API Keys

For enhanced security, use Codespace secrets instead of .env files:

### Setting Up Secrets

1. Go to GitHub Settings → Codespaces → Secrets
2. Click **"New secret"**
3. Add your secrets:
   - Name: `OPENAI_API_KEY`
   - Value: `sk-your-key-here`

### Accessing Secrets in Your Codespace

Secrets are automatically available as environment variables:

```bash
# No need for .env file - just use the environment variable
python main.py
```

Update `backend/main.py` to read from environment:

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

## Codespace Features

### Port Forwarding

Ports are automatically forwarded and accessible:
- **Port 3000**: Frontend (Next.js)
- **Port 8000**: Backend (FastAPI)

### VS Code Extensions

Pre-installed extensions:
- Python tools (Pylance, Black formatter)
- JavaScript/TypeScript tools (ESLint, Prettier)
- React development support
- Tailwind CSS IntelliSense

### Terminal Access

Multiple terminals for running:
- Backend server
- Frontend dev server
- Additional commands (tests, linting, etc.)

## Codespace Configuration

The configuration is defined in `.devcontainer/generative-ui/devcontainer.json`:

- **Base image**: `mcr.microsoft.com/devcontainers/python:3.11`
- **Node.js**: Version 20
- **Features**: Git, Git LFS, common utilities
- **Ports**: 3000 (frontend), 8000 (backend)

## Troubleshooting Codespaces

### Issue: Codespace Won't Start

**Solution:**
- Check your GitHub account has Codespace quota
- Try creating a new codespace
- Check GitHub status page

### Issue: Can't Access Application

**Solution:**
- Ensure ports are forwarded (check "Ports" tab)
- Verify services are running in terminals
- Check port visibility is set to "Public" or "Private to Organization"

### Issue: Changes Not Persisting

**Solution:**
- Codespaces auto-save, but check the file has saved
- Commit changes to Git to preserve them
- Don't close codespace while processes are running

### Issue: Performance Problems

**Solution:**
- Upgrade codespace machine type (Settings → Machine type)
- Close unused applications/tabs
- Restart the codespace

## Best Practices

1. **Save Your Work**: Commit frequently to Git
2. **Use Secrets**: Store API keys in Codespace secrets
3. **Stop When Not in Use**: Codespaces auto-stop after inactivity
4. **Resource Management**: Stop services you're not using
5. **Regular Updates**: Pull latest changes from main branch

## Advanced: Customizing Your Codespace

### Modify the Devcontainer

Edit `.devcontainer/generative-ui/devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        // Add your favorite extensions
        "example.extension-id"
      ]
    }
  }
}
```

### Add Custom Setup Scripts

Edit `.devcontainer/generative-ui/setup.sh`:

```bash
#!/bin/bash

# Your custom setup commands
pip install your-package
npm install -g your-tool
```

### Rebuild the Devcontainer

After changes:
1. Press `F1` or `Cmd/Ctrl + Shift + P`
2. Search for "Rebuild Container"
3. Wait for rebuild to complete

## Cost and Limits

- GitHub provides free Codespace hours for personal accounts
- Check your quota: GitHub Settings → Billing → Codespaces
- Codespaces auto-stop after 30 minutes of inactivity
- Delete unused codespaces to free up quota

## Next Steps

Once your codespace is running:

1. ✅ Complete the [Getting Started Guide](templates/generative-ui/GETTING_STARTED.md)
2. ✅ Try the [Examples](templates/generative-ui/examples/README.md)
3. ✅ Customize components and agents
4. ✅ Build your application!

## Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [AG2 Documentation](https://docs.ag2.ai/)
- [Generative UI Template README](templates/generative-ui/README.md)

Happy coding! 🚀
