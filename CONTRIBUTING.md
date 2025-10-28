# Contributing to BotSmith

First off, thank you for considering contributing to BotSmith! It's people like you that make BotSmith such a great tool.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Messages](#commit-messages)
6. [Pull Request Process](#pull-request-process)
7. [Bug Reports](#bug-reports)
8. [Feature Requests](#feature-requests)
9. [Documentation](#documentation)
10. [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at conduct@botsmith.ai. All complaints will be reviewed and investigated promptly and fairly.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Ubuntu 22.04]
 - Browser: [e.g., Chrome 120]
 - Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

**Feature Request Template:**
```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Mockups, examples, or other relevant information.
```

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues for beginners
- `help wanted` - Issues where we need community help
- `bug` - Known bugs that need fixing
- `documentation` - Documentation improvements

### Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue that pull request!

---

## Development Setup

### Prerequisites

```bash
# Check versions
python --version  # 3.11+
node --version    # 18+
yarn --version    # 1.22+
mongod --version  # 6.0+
```

### Setup Steps

**1. Fork and Clone**
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/botsmith.git
cd botsmith
git remote add upstream https://github.com/original-org/botsmith.git
```

**2. Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dev dependencies
cp .env.example .env
# Edit .env with your configuration
```

**3. Frontend Setup**
```bash
cd frontend
yarn install
cp .env.example .env
# Edit .env with your configuration
```

**4. Database Setup**
```bash
# Start MongoDB
mongod --dbpath /data/db

# Create database (in mongo shell)
mongo
> use botsmith
> db.createCollection('users')
> exit
```

**5. Start Development Servers**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
yarn start
```

**6. Verify Setup**
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8001/docs

---

## Coding Standards

### Python (Backend)

**Style Guide:**
- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Maximum line length: 100 characters

**Example:**
```python
from typing import List, Optional
from fastapi import HTTPException

async def get_chatbots(
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    """
    Retrieve chatbots for a user.
    
    Args:
        user_id: The user's unique identifier
        skip: Number of records to skip
        limit: Maximum records to return
        
    Returns:
        List of chatbot dictionaries
        
    Raises:
        HTTPException: If user not found
    """
    chatbots = await db.chatbots.find(
        {"user_id": user_id}
    ).skip(skip).limit(limit).to_list(limit)
    
    return chatbots
```

**Formatting:**
```bash
# Format code with Black
black .

# Check with Flake8
flake8 .

# Type checking with mypy
mypy .
```

### JavaScript/React (Frontend)

**Style Guide:**
- Use functional components with hooks
- Use const/let, never var
- Use arrow functions
- Destructure props
- Use meaningful variable names

**Example:**
```javascript
import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';

const ChatbotList = ({ userId }) => {
  const [chatbots, setChatbots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChatbots = async () => {
      try {
        const response = await api.get('/api/chatbots');
        setChatbots(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChatbots();
  }, [userId]);

  if (loading) return <Loading />;
  if (error) return <Error message={error} />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {chatbots.map((chatbot) => (
        <ChatbotCard key={chatbot.id} chatbot={chatbot} />
      ))}
    </div>
  );
};

export default ChatbotList;
```

**Formatting:**
```bash
# Format with Prettier
yarn run prettier --write src/

# Lint with ESLint
yarn run eslint src/
```

### CSS/Tailwind

**Guidelines:**
- Use Tailwind utility classes
- Group related classes
- Use responsive prefixes (sm:, md:, lg:)
- Extract repeated patterns to components

**Example:**
```jsx
{/* Good */}
<button className="
  px-6 py-3 
  bg-gradient-to-r from-purple-600 to-pink-600 
  text-white font-semibold 
  rounded-lg shadow-lg 
  hover:shadow-xl hover:scale-105 
  transition-all duration-200
  focus:outline-none focus:ring-2 focus:ring-purple-500
">
  Create Chatbot
</button>

{/* Bad */}
<button style={{padding: '12px 24px', backgroundColor: '#9333ea'}}>
  Create Chatbot
</button>
```

---

## Commit Messages

### Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Code style (formatting, missing semicolons, etc.)
- **refactor**: Code restructuring
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **ci**: CI/CD changes

### Examples

**Good:**
```
feat(chatbots): add model selection dropdown

- Added support for multiple AI providers
- Users can now choose between OpenAI, Claude, and Gemini
- Updated API to accept model parameter

Closes #123
```

```
fix(auth): resolve token expiration issue

Fixed bug where tokens were expiring too quickly.
Updated JWT_EXPIRE_MINUTES to correct value.

Fixes #456
```

```
docs(api): update endpoint documentation

Added examples for all chat endpoints.
Clarified authentication requirements.
```

**Bad:**
```
Fixed stuff
Update
WIP
```

---

## Pull Request Process

### Before Submitting

**1. Create a Branch**
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/annoying-bug
```

**2. Make Your Changes**
- Write code
- Add/update tests
- Update documentation
- Follow coding standards

**3. Test Your Changes**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
yarn test

# Manual testing
# Test in browser, try different scenarios
```

**4. Commit Your Changes**
```bash
git add .
git commit -m "feat(scope): descriptive message"
```

**5. Push to Your Fork**
```bash
git push origin feature/amazing-feature
```

### Submitting

**1. Create Pull Request**
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Fill out the template

**PR Template:**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe testing performed.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally

## Screenshots (if applicable)

## Related Issues
Closes #123
```

**2. Review Process**
- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

**3. After Merge**
```bash
# Update your fork
git checkout main
git pull upstream main
git push origin main
```

---

## Bug Reports

### Good Bug Report Checklist

- [ ] Descriptive title
- [ ] Clear reproduction steps
- [ ] Expected vs actual behavior
- [ ] Environment details
- [ ] Screenshots/videos if applicable
- [ ] Error messages/logs
- [ ] Checked for existing issues

### Example Bug Report

```markdown
**Title:** Chatbot creation fails with special characters in name

**Description:**
When creating a chatbot with special characters (e.g., "My Bot #1"),
the API returns a 500 error.

**Steps to Reproduce:**
1. Go to Dashboard
2. Click "Create New"
3. Enter name "My Bot #1"
4. Click "Create"
5. See error message

**Expected Behavior:**
Chatbot should be created successfully with the given name.

**Actual Behavior:**
API returns 500 error. Console shows:
```
Error: Invalid character in chatbot name
```

**Environment:**
- OS: macOS 13.0
- Browser: Chrome 120.0
- Version: 1.0.0

**Screenshots:**
[Attach screenshot]

**Additional Context:**
Workaround: Remove special characters from name.
```

---

## Feature Requests

### Good Feature Request Checklist

- [ ] Clear problem statement
- [ ] Proposed solution
- [ ] Alternative solutions considered
- [ ] Use cases
- [ ] Mockups/examples if applicable
- [ ] Checked for existing requests

### Example Feature Request

```markdown
**Title:** Add conversation export to CSV

**Problem:**
Users want to analyze conversations in spreadsheet tools like Excel,
but currently can only export to JSON.

**Proposed Solution:**
Add CSV export option alongside JSON in the Export menu.
CSV should include:
- Timestamp
- User name
- User message
- Bot response
- Response time

**Alternatives Considered:**
1. Export to Google Sheets directly (complex, requires auth)
2. Export to PDF (not suitable for analysis)

**Use Cases:**
- Marketing teams analyzing customer inquiries
- Support teams tracking response quality
- Data analysts building reports

**Mockup:**
[Attach mockup image]

**Additional Context:**
Many users have requested this in support tickets.
```

---

## Documentation

### Types of Documentation

1. **Code Comments**: Explain complex logic
2. **API Docs**: Endpoint documentation
3. **User Guides**: How-to guides for users
4. **Developer Guides**: Setup and architecture
5. **README**: Project overview

### Documentation Standards

**API Documentation:**
```python
@router.post("/chatbots")
async def create_chatbot(
    chatbot: ChatbotCreate,
    user: User = Depends(get_current_user)
) -> ChatbotResponse:
    """
    Create a new chatbot.
    
    **Parameters:**
    - name: Chatbot name (required)
    - model: AI model to use (required)
    - provider: AI provider (openai/anthropic/google)
    - system_message: Custom system prompt
    
    **Returns:**
    - ChatbotResponse with id and creation details
    
    **Raises:**
    - 400: Invalid input
    - 401: Unauthorized
    - 403: Plan limit reached
    """
    # Implementation
```

**README Sections:**
- Clear project description
- Installation instructions
- Quick start guide
- Links to detailed docs
- Contribution guidelines
- License information

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, announcements
- **Discord**: Real-time chat (coming soon)
- **Email**: support@botsmith.ai

### Getting Help

**Before Asking:**
1. Check existing documentation
2. Search closed issues
3. Try the troubleshooting guide

**When Asking:**
- Provide context
- Share relevant code/logs
- Describe what you've tried
- Be respectful and patient

### Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Special thanks in README
- Community showcase

---

## License

By contributing to BotSmith, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

Don't hesitate to reach out:
- **Email**: contribute@botsmith.ai
- **GitHub Issues**: [Ask a question](https://github.com/your-org/botsmith/issues/new?labels=question)
- **Discussions**: [Start a discussion](https://github.com/your-org/botsmith/discussions)

---

**Thank you for contributing to BotSmith!** 🎉

Your time and effort make this project better for everyone.