# Contributing to Generative UI Template

Thank you for your interest in contributing! This template is part of the AG2 ecosystem and follows similar contribution guidelines.

## Ways to Contribute

### 1. Report Issues
- Bug reports
- Feature requests
- Documentation improvements
- UX/UI suggestions

### 2. Submit Code
- Bug fixes
- New features
- Performance improvements
- New agent examples
- UI component enhancements

### 3. Improve Documentation
- Fix typos
- Add examples
- Clarify instructions
- Write tutorials

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## Code Standards

### Python Code
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Add tests for new features

### JavaScript Code
- Use modern ES6+ syntax
- Follow consistent naming conventions
- Comment complex logic
- Ensure browser compatibility

### UI/UX
- Follow accessibility guidelines (WCAG 2.1 AA)
- Ensure responsive design
- Maintain consistent styling
- Test on multiple browsers

## Pull Request Process

1. **Create a Branch**: Use descriptive names
   - `feature/add-new-chart-type`
   - `fix/form-validation-bug`
   - `docs/update-quickstart`

2. **Make Changes**: Keep commits focused and atomic

3. **Test**: Ensure all tests pass and add new tests if needed

4. **Document**: Update README or docs if needed

5. **Submit PR**: 
   - Clear title and description
   - Reference related issues
   - Describe what changed and why

6. **Review**: Address feedback from reviewers

## Adding New Agents

When adding a new agent type:

1. Create the agent file in `agents/` directory
2. Add proper docstrings explaining the agent's purpose
3. Register necessary tools
4. Add configuration to `config/agent_config.yaml`
5. Update README with usage examples
6. Add tests

Example:
```python
def create_my_agent() -> ConversableAgent:
    """
    Create an agent that does X.
    
    This agent specializes in Y and can:
    1. Do task A
    2. Do task B
    """
    system_message = """..."""
    # ... implementation
```

## Adding New UI Components

When adding new UI components:

1. Add component template to `config/ui_templates.json`
2. Implement renderer in `frontend/static/js/app.js`
3. Add necessary CSS to `frontend/static/css/styles.css`
4. Update `backend/ui_generator.py` if needed
5. Add examples to the documentation

## Testing

Before submitting:
- Test with different API providers (OpenAI, Anthropic, etc.)
- Test UI in multiple browsers
- Check accessibility
- Verify mobile responsiveness
- Test error handling

## Questions?

- Check the [AG2 Documentation](https://docs.ag2.ai/)
- Join the [AG2 Discord](https://discord.gg/pAbnFJrkgZ)
- Open a discussion on GitHub

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache 2.0).
