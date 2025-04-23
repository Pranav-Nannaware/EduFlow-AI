# Contributing to EduFlow AI

Thank you for your interest in contributing to EduFlow AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Documentation Guidelines](#documentation-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

We expect all contributors to follow our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the Repository**
   - Visit the [EduFlow AI repository](https://github.com/yourusername/eduflow-ai)
   - Click the "Fork" button to create your own copy

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/eduflow-ai.git
   cd eduflow-ai
   ```

3. **Set Up the Development Environment**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. **Keep Your Fork Updated**
   ```bash
   git remote add upstream https://github.com/original-owner/eduflow-ai.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Make Your Changes**
   - Implement your feature or fix
   - Write or update tests
   - Update documentation as needed

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description of changes"
   ```
   
   Commit messages should be clear and descriptive, starting with an action verb like "Add", "Fix", "Update", etc.

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select "compare across forks"
   - Select your fork and branch

2. **PR Template**
   Fill out the pull request template with:
   - A clear description of the changes
   - Link to any related issues
   - Screenshots if applicable
   - Checklist of completed items

3. **Code Review**
   - Address any feedback or comments from reviewers
   - Make necessary changes and push them to your branch

4. **Merging**
   - A maintainer will merge your PR once it's approved
   - Your contribution will be part of the project!

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints when possible
- Document functions and classes with docstrings
- Keep functions focused (single responsibility)
- Write descriptive variable names

```python
# Good example
def calculate_quiz_score(answers: List[str], correct_answers: List[str]) -> float:
    """
    Calculate the percentage score for a quiz.
    
    Args:
        answers: List of user answers
        correct_answers: List of correct answers
        
    Returns:
        The percentage score (0-100)
    """
    if not answers or not correct_answers:
        return 0.0
        
    correct_count = sum(1 for a, b in zip(answers, correct_answers) if a == b)
    return (correct_count / len(correct_answers)) * 100
```

### HTML/CSS/JavaScript

- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use 2-space indentation for HTML and CSS
- Keep CSS classes meaningful and following BEM naming convention when possible
- Use semantic HTML elements

## Documentation Guidelines

- Always update documentation when changing functionality
- Keep README and documentation files up-to-date
- Use markdown for documentation files
- Include code examples when explaining APIs or functions
- Document any environment variables or configuration options

## Testing Guidelines

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a PR
- Aim for good test coverage (at least 70%)
- Include both unit tests and integration tests where appropriate

### Test Structure

```python
def test_user_registration_valid_data():
    """Test user registration with valid input data."""
    # Arrange
    test_data = {
        'username': 'testuser',
        'name': 'Test User',
        'age': '25',
        'language': 'English'
    }
    
    # Act
    with app.test_client() as client:
        response = client.post('/register', data=test_data)
    
    # Assert
    assert response.status_code == 302  # Redirect
    assert 'user_id' in session
```

## Issue Reporting

If you find a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue if needed
3. Use the provided templates
4. Include as much information as possible:
   - For bugs: steps to reproduce, expected behavior, actual behavior, screenshots
   - For features: clear description, use cases, acceptance criteria

## Feature Development Process

1. **Propose Your Idea**
   - Open an issue with the "feature request" template
   - Discuss the feature with maintainers
   
2. **Design Phase**
   - Create a design document if needed
   - Get feedback on the approach
   
3. **Implementation**
   - Follow the development workflow
   - Keep changes focused on the specific feature
   
4. **Testing**
   - Add appropriate tests
   - Test edge cases
   
5. **Documentation**
   - Update or add documentation
   - Include usage examples

## Project Structure Updates

When adding new components to the project:

1. Follow the existing structure
2. Update the architecture documentation
3. Add appropriate tests
4. Update import statements in affected files

## AI Features Guidelines

When working with AI integration features:

1. Ensure prompts are clear and specific
2. Handle API errors gracefully
3. Implement rate limiting and caching where appropriate
4. Test with varied inputs to ensure robustness
5. Document API usage and expectations

## Performance Considerations

- Profile your code for performance bottlenecks
- Be mindful of memory usage
- Consider the impact of your changes on application speed
- Optimize database or file operations for efficiency

## Accessibility

We strive to make EduFlow AI accessible to all users:

- Use semantic HTML
- Include appropriate ARIA attributes
- Ensure sufficient color contrast
- Support keyboard navigation
- Test with screen readers when possible

---

Thank you for contributing to EduFlow AI! Your efforts help make education more accessible and personalized for learners worldwide. 