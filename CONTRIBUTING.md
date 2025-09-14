# Contributing to CodeLion

Thank you for your interest in contributing to CodeLion! 🦁

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/coderlion.git
   cd coderlion
   ```

3. **Set up the development environment**:
   ```bash
   # Copy environment file
   cp env.example .env
   
   # Start with Docker
   docker-compose up -d
   ```

4. **Update your .env file** with your API keys:
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a GitHub OAuth app for authentication
   - Update the configuration in `.env`

## Development

### Backend Development

The backend is built with FastAPI and includes:
- **Multi-agent architecture** for code analysis
- **GitHub integration** for webhook handling
- **Gemini AI integration** for intelligent code review
- **PostgreSQL** for data persistence
- **Redis** for caching and job queues

### Frontend Development

The frontend is built with Next.js 14 and includes:
- **Modern React** with TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** components
- **Real-time updates** for agent progress

### Adding New Agents

1. Create a new agent class in `backend/app/agents/`
2. Inherit from `BaseAgent` and implement required methods
3. Register the agent in `AgentRegistry`
4. Add agent-specific UI components in the frontend

Example:
```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="custom",
            description="Custom analysis agent"
        )
    
    async def analyze(self, code_diff: str, context: Dict[str, Any]) -> AgentResult:
        # Your analysis logic here
        pass
    
    def get_system_prompt(self) -> str:
        return "Your custom system prompt"
```

## Testing

Run tests with:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** with clear commit messages
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict mode, prefer functional components
- **Commits**: Use conventional commit messages
- **Documentation**: Update README and code comments

## Issues

- **Bug reports**: Use the bug report template
- **Feature requests**: Use the feature request template
- **Questions**: Use GitHub Discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Community

- **Discord**: Join our community server
- **Twitter**: Follow [@CodeLionAI](https://twitter.com/CodeLionAI)
- **GitHub Discussions**: Ask questions and share ideas

Thank you for contributing to CodeLion! 🚀
