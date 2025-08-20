# Contributing to NAVI

Thank you for your interest in contributing to NAVI! We welcome contributions from everyone and appreciate your help in making NAVI better.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
Found a bug? We'd love to hear about it! Please:
- Check existing issues first
- Provide clear reproduction steps
- Include system information
- Add relevant logs or screenshots

### ✨ Feature Requests
Have an idea for a new feature? Great! Please:
- Describe the problem you're solving
- Explain the proposed solution
- Consider backwards compatibility
- Discuss potential alternatives

### 🔧 Code Contributions
Ready to dive into the code? Awesome! Here's how:

#### Getting Started
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/Navi.git
cd Navi

# Create virtual environment
python3 -m venv navi_env
source navi_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks (optional)
pre-commit install
```

#### Development Workflow
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Run tests
python -m pytest tests/

# Run linting
black navi/ tests/
flake8 navi/ tests/

# Commit your changes
git commit -m "Add: your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

### 📚 Documentation
Help improve our documentation:
- Fix typos or unclear explanations
- Add examples and use cases
- Translate to other languages
- Create video tutorials

### 🧪 Testing
Help ensure NAVI is reliable:
- Write unit tests
- Add integration tests
- Test on different platforms
- Report compatibility issues

## 🎯 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all public functions
- Keep functions small and focused
- Use type hints where appropriate

### Commit Messages
Use clear, descriptive commit messages:
```
Add: new feature X
Fix: bug in Y component
Docs: update installation guide
Refactor: simplify Z module
Test: add tests for W functionality
```

### Pull Request Process
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Document** new features
6. **Submit** pull request with clear description

### Code Review
All contributions go through code review:
- Be patient and open to feedback
- Address review comments promptly
- Keep discussions constructive
- Learn from the process

## 🚀 Development Setup

### Project Structure
```
navi/
├── core.py          # Main application logic
├── providers.py     # AI provider abstractions
├── agents.py        # Specialized AI agents
├── memory.py        # Memory and context management
└── __init__.py

cli/
└── navi_cli.py      # Command-line interface

config/
├── settings.yaml    # Configuration files
├── agents.yaml
├── providers.yaml
└── memory.yaml

tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── fixtures/       # Test data

docs/
├── api/           # API documentation
├── guides/        # User guides
└── development/   # Development docs
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_agents.py

# Run with coverage
python -m pytest --cov=navi tests/

# Run integration tests
python -m pytest tests/integration/
```

### Local Development
```bash
# Run NAVI in development mode
python -m navi.core --debug

# Run with specific provider
python -m navi.core --provider ollama

# Test CLI interface
python cli/navi_cli.py --status
```

## 📋 Issue Templates

### Bug Report Template
```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.11.0]
- NAVI: [e.g. 2.0.0]
```

### Feature Request Template
```markdown
**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
Describe your solution idea.

**Alternatives Considered**
Other approaches you've thought about.

**Additional Context**
Any other context or screenshots.
```

## 🎨 Design Principles

### Local-First
- Prioritize local processing
- Make cloud features optional
- Respect user privacy
- Minimize data transmission

### Modularity
- Keep components loosely coupled
- Use clear interfaces
- Enable easy extensibility
- Support plugin architecture

### User Experience
- Prioritize ease of use
- Provide helpful error messages
- Support multiple interfaces
- Maintain consistency

### Performance
- Optimize for responsiveness
- Minimize resource usage
- Support streaming responses
- Enable async operations

## 🌍 Internationalization

Help translate NAVI:
- Create language files in `i18n/`
- Follow existing structure
- Test with different locales
- Update documentation

Current languages:
- English (primary)
- Swedish (partial)

Wanted languages:
- German
- French
- Spanish
- Japanese
- Chinese

## 📞 Getting Help

Need help contributing? We're here to help!

- 📖 Read the [Development Guide](docs/development.md)
- 💬 Join our [Discord community](https://discord.gg/navi-ai)
- 📧 Email us at bjornshomelab@gmail.com
- 🐛 Open an issue on GitHub

## 🏆 Recognition

Contributors will be:
- Listed in our README
- Featured in release notes
- Invited to our contributors chat
- Eligible for special badges

## 📄 License

By contributing to NAVI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to NAVI! Together, we're building the future of local-first AI. 🤖✨
