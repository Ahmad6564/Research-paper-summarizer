# Contributing to Research Paper Summarizer

Thank you for your interest in contributing to the Research Paper Summarizer! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/paper-summarizer.git
   cd paper-summarizer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## 🔧 Development Setup

### Running Tests
```bash
python -m pytest test_summarizer.py -v
```

### Running the Application
```bash
# Web interface
python app.py

# Command line interface
python cli.py --help
```

## 📝 Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## 🐛 Bug Reports

When filing a bug report, please include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Any error messages or logs

## ✨ Feature Requests

For new features:
- Describe the use case and motivation
- Provide examples of how it would work
- Consider backward compatibility
- Discuss implementation approach

## 🔄 Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Update documentation if needed

4. Commit with clear, descriptive messages:
   ```bash
   git commit -m "Add support for new paper format"
   ```

5. Push to your fork and create a pull request

6. Ensure all tests pass and address any review feedback

## 📋 Summary Format Guidelines

When modifying the summary generation:
- Maintain the structured template format with emojis
- Preserve academic rigor and faithfulness to source material
- Test with various paper types (ML, physics, biology, etc.)
- Ensure consistent markdown formatting

## 🧪 Testing

- Add tests for new functionality
- Ensure existing tests still pass
- Test with real papers from different domains
- Verify both markdown and JSON outputs

## 📚 Documentation

- Update README.md for user-facing changes
- Add inline code comments for complex logic
- Update API documentation for new endpoints
- Include usage examples

## ❓ Questions?

Feel free to open an issue for questions about contributing or reach out to the maintainers.

Thank you for helping make this project better! 🎉
