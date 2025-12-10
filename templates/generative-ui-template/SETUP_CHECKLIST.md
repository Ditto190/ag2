# Setup Checklist

Use this checklist to ensure your Generative UI template is properly configured.

## 📋 Pre-Setup

- [ ] Python 3.10, 3.11, 3.12, or 3.13 installed
- [ ] Git installed (for cloning)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] OpenAI API key or other LLM provider key

## 🚀 Initial Setup

### 1. Get the Template
- [ ] Clone the repository or copy the template directory
- [ ] Navigate to `templates/generative-ui-template`

### 2. Environment Setup
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
  - [ ] macOS/Linux: `source venv/bin/activate`
  - [ ] Windows: `venv\Scripts\activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

### 3. API Configuration
Choose one method:

**Option A: Environment Variable**
- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Verify: `echo $OPENAI_API_KEY` (macOS/Linux) or `echo %OPENAI_API_KEY%` (Windows)

**Option B: Config File**
- [ ] Copy `OAI_CONFIG_LIST.example` to `OAI_CONFIG_LIST`
- [ ] Edit `OAI_CONFIG_LIST` with your API key
- [ ] Verify file exists and contains valid JSON

### 4. Validation
- [ ] Run validation script: `python validate.py`
- [ ] All checks should pass (5/5)
- [ ] Fix any failed checks before proceeding

## 🧪 Testing

### 5. Start the Application
- [ ] Run: `python backend/main.py`
- [ ] Server starts without errors
- [ ] Server running on http://localhost:8000
- [ ] No import errors or exceptions

### 6. Test in Browser
- [ ] Open http://localhost:8000
- [ ] Page loads successfully
- [ ] No JavaScript console errors
- [ ] CSS styles are applied

### 7. Test UI Generation
- [ ] Enter a test prompt (e.g., "create a contact form")
- [ ] Click "Generate UI" button
- [ ] UI generates without errors
- [ ] Generated component displays correctly

### 8. Test Example Buttons
- [ ] Click "Contact Form" example
- [ ] Form UI generates
- [ ] Click "Dashboard" example
- [ ] Dashboard UI generates
- [ ] Click "Data Table" example
- [ ] Table UI generates

## 🔧 Optional Setup

### 9. Docker Setup (Optional)
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Run: `docker-compose up`
- [ ] Application accessible at http://localhost:8000

### 10. GitHub Codespaces (Optional)
- [ ] Repository is on GitHub
- [ ] Create new Codespace
- [ ] Codespace builds successfully
- [ ] Application runs in Codespace

### 11. Frontend Development (Optional)
- [ ] Node.js installed (v18+)
- [ ] Run: `npm install`
- [ ] Optional dependencies installed

## 🎨 Customization Checklist

### 12. Customize Agents
- [ ] Review `backend/agents.py`
- [ ] Modify system messages as needed
- [ ] Adjust temperature and parameters
- [ ] Test agent responses

### 13. Customize UI
- [ ] Review `frontend/static/css/styles.css`
- [ ] Update color scheme in `:root` variables
- [ ] Modify component styles as needed
- [ ] Test responsive design

### 14. Add Custom Tools
- [ ] Review `backend/tools.py`
- [ ] Add your custom tools
- [ ] Register tools with agents
- [ ] Test tool execution

### 15. Configure Templates
- [ ] Review `config/ui_templates.json`
- [ ] Add or modify component templates
- [ ] Update `config/agent_config.yaml`
- [ ] Test configuration loading

## 📚 Learning & Documentation

### 16. Review Documentation
- [ ] Read `README.md` completely
- [ ] Review `QUICKSTART.md`
- [ ] Check `USECASES.md` for ideas
- [ ] Read `CONTRIBUTING.md` if planning to contribute

### 17. Run Examples
- [ ] Review `examples/task_manager.py`
- [ ] Run: `python examples/task_manager.py`
- [ ] Understand the example patterns
- [ ] Adapt for your use case

## 🚢 Deployment Checklist

### 18. Production Preparation
- [ ] Set production API keys
- [ ] Update `RELOAD=false` in environment
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up error logging
- [ ] Configure rate limiting (if needed)

### 19. Security Review
- [ ] API keys stored securely (not in code)
- [ ] `.env` file in `.gitignore`
- [ ] No sensitive data in frontend
- [ ] HTTPS enabled in production
- [ ] CORS configured properly

### 20. Performance Optimization
- [ ] Test with realistic data volumes
- [ ] Monitor API call costs
- [ ] Implement caching if needed
- [ ] Optimize agent response times

## ✅ Final Verification

- [ ] Application runs without errors
- [ ] UI generation works consistently
- [ ] All examples work correctly
- [ ] Documentation is clear
- [ ] Ready to build your application!

## 🆘 Troubleshooting

If you encounter issues:

1. **Check validation**: Run `python validate.py`
2. **Review logs**: Check console output for errors
3. **Verify API keys**: Ensure they're set correctly
4. **Check dependencies**: Reinstall with `pip install -r requirements.txt`
5. **Consult docs**: Review README.md and QUICKSTART.md
6. **Get help**: 
   - AG2 Discord: https://discord.gg/pAbnFJrkgZ
   - AG2 Docs: https://docs.ag2.ai/
   - GitHub Issues: https://github.com/ag2ai/ag2/issues

## 🎉 Ready to Go!

Once all checks are complete, you're ready to start building amazing Generative UI applications with AG2!

Next steps:
1. Explore the `USECASES.md` file for inspiration
2. Review `examples/task_manager.py` for implementation patterns
3. Start building your own application
4. Share your creation with the AG2 community!

Happy coding! 🚀
