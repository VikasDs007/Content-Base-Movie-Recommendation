# Contributing to CineMatch 🎭

Thank you for your interest in contributing to CineMatch! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of machine learning and web development

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/cinematch-ai-recommendations.git
   cd cinematch-ai-recommendations
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🎯 How to Contribute

### 🐛 Bug Reports

When reporting bugs, please include:
- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **System information** (OS, Python version, browser)
- **Screenshots** if applicable

Use this template:
```markdown
**Bug Description:**
A clear description of what the bug is.

**To Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen.

**System Info:**
- OS: [e.g., Windows 10, macOS 12.0]
- Python: [e.g., 3.9.7]
- Browser: [e.g., Chrome 96.0]
```

### ✨ Feature Requests

For new features, please:
- **Check existing issues** to avoid duplicates
- **Describe the feature** clearly
- **Explain the use case** and benefits
- **Consider implementation complexity**

### 🔧 Code Contributions

#### Code Style Guidelines

- **Follow PEP 8** for Python code style
- **Use meaningful variable names**
- **Add docstrings** to all functions and classes
- **Include type hints** where appropriate
- **Keep functions small** and focused
- **Write comments** for complex logic

Example:
```python
def calculate_similarity(movie_vector: np.ndarray, all_vectors: np.ndarray) -> np.ndarray:
    """
    Calculate cosine similarity between a movie and all other movies.
    
    Args:
        movie_vector: TF-IDF vector for the input movie
        all_vectors: TF-IDF vectors for all movies in the database
        
    Returns:
        Array of similarity scores
    """
    return cosine_similarity(movie_vector, all_vectors).flatten()
```

#### Testing

- **Test your changes** thoroughly
- **Add unit tests** for new functions
- **Ensure existing tests pass**
- **Test on different datasets** if possible

#### Commit Messages

Use clear, descriptive commit messages:
```bash
# Good
git commit -m "Add fuzzy search functionality for movie titles"
git commit -m "Fix similarity calculation for empty descriptions"
git commit -m "Improve UI responsiveness on mobile devices"

# Bad
git commit -m "Fix bug"
git commit -m "Update code"
git commit -m "Changes"
```

## 📋 Development Areas

### 🎨 Frontend/UI
- Improve user interface design
- Add new interactive features
- Enhance mobile responsiveness
- Create better visualizations

### 🤖 Machine Learning
- Improve recommendation algorithms
- Add new similarity metrics
- Implement collaborative filtering
- Optimize performance

### 🔧 Backend/Infrastructure
- Add API endpoints
- Improve caching mechanisms
- Database optimizations
- Error handling

### 📖 Documentation
- Improve README
- Add code comments
- Create tutorials
- Write API documentation

## 🎯 Priority Areas

We're especially looking for contributions in:

1. **Algorithm Improvements**
   - Hybrid recommendation systems
   - Better text preprocessing
   - Advanced similarity metrics

2. **User Experience**
   - Better search functionality
   - User preference learning
   - Recommendation explanations

3. **Performance**
   - Faster similarity computation
   - Better memory management
   - Caching optimizations

4. **Features**
   - User accounts and favorites
   - Movie poster integration
   - Advanced filtering options

## 🔍 Code Review Process

1. **Submit a Pull Request** with a clear description
2. **Ensure all tests pass** and code follows guidelines
3. **Respond to feedback** from maintainers
4. **Make requested changes** promptly
5. **Celebrate** when your PR is merged! 🎉

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏷️ Issue Labels

We use these labels to organize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority-high` - High priority items
- `ui/ux` - User interface improvements
- `algorithm` - ML algorithm improvements

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Respect different viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Collaborative
- Help others learn and grow
- Share knowledge and resources
- Provide constructive feedback
- Celebrate others' contributions

### Be Professional
- Keep discussions on-topic
- Avoid personal attacks or harassment
- Use appropriate language
- Follow the code of conduct

## 📞 Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Ask in discussions** for general questions
4. **Create an issue** for specific problems
5. **Join our Discord** for real-time chat

## 🎉 Recognition

Contributors will be:
- **Listed in README** acknowledgments
- **Mentioned in release notes** for significant contributions
- **Invited to join** the core team for outstanding contributions
- **Featured on social media** for major features

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CineMatch! Your efforts help make movie discovery better for everyone. 🎬✨