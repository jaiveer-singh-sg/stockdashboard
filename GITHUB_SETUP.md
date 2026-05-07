# GitHub Repository Setup Guide

## Create GitHub Repository

### Option 1: Using GitHub Web Interface

1. **Go to GitHub**: https://github.com/new

2. **Create Repository**
   - Repository name: `StocksDashboard` (or your preferred name)
   - Description: "Comprehensive NASDAQ stock analysis dashboard with real-time data from TradingView and Yahoo Finance"
   - Choose visibility: Public or Private
   - Do NOT initialize with README, .gitignore, or license (we already have these)

3. **Get Repository URL**
   - Copy the HTTPS or SSH URL

### Option 2: Using GitHub CLI

```bash
# Install GitHub CLI (if not already installed)
# https://cli.github.com/

# Authenticate
gh auth login

# Create repository
gh repo create StocksDashboard --public --source=. --remote=origin --push
```

## Push Existing Repository to GitHub

### Using HTTPS (easier if you don't have SSH setup)

```bash
cd D:\Sandbox\AI Code\StocksDashboard

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/StocksDashboard.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Using SSH (more secure)

```bash
# Add remote origin
git remote add origin git@github.com:YOUR_USERNAME/StocksDashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Complete Repository Setup

### 1. Add GitHub Actions Workflow

Create `.github/workflows/python-app.yml`:

```yaml
name: Python Application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check code with pylint
      run: |
        pip install pylint
        pylint app/ --exit-zero
```

### 2. Add Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows, Linux, Mac]
 - Python Version: [e.g. 3.9]
 - Browser: [e.g. Chrome, Firefox]

**Additional context**
Add any other context about the problem here.
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''

---

**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### 3. Add Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Related Issue
Fixes # (issue)

## Testing
- [ ] I have tested my changes locally
- [ ] All existing tests pass
- [ ] New tests added

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
```

### 4. Setup Branch Protection Rules

1. Go to Repository Settings
2. Select "Branches"
3. Add branch protection rule for `main`:
   - Require pull request reviews before merging
   - Require status checks to pass
   - Dismiss stale pull request approvals
   - Require branches to be up to date before merging

### 5. Add Collaborators & Teams (if applicable)

1. Go to Repository Settings
2. Select "Collaborators"
3. Add team members with appropriate permissions

## Git Workflow

### For Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: Add new feature description"

# Push to origin
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change without feature/bug changes
- `perf`: Performance improvements
- `test`: Adding or updating tests

Example:
```
feat(chart): Add MACD indicator to chart view

Added MACD indicator calculation and visualization to the technical chart.
Includes signal line and histogram for better trend analysis.

Fixes #123
```

## Adding a License

Choose a license and add it:

```bash
# MIT License (recommended for educational projects)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "docs: Add MIT License"
git push origin main
```

## Repository Badges

Add to README.md:

```markdown
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![Flask](https://img.shields.io/badge/flask-2.3%2B-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Actions](https://github.com/YOUR_USERNAME/StocksDashboard/workflows/Python%20Application/badge.svg)](https://github.com/YOUR_USERNAME/StocksDashboard/actions)

```

## Final Verification

1. Visit your GitHub repository: `https://github.com/YOUR_USERNAME/StocksDashboard`
2. Verify all files are pushed
3. Check Actions tab for workflow runs
4. Review Insights for analytics

## Pushing Updates

```bash
# After making local changes
git add .
git commit -m "feat: description of changes"
git push origin main
```

## Cloning for Others

```bash
git clone https://github.com/YOUR_USERNAME/StocksDashboard.git
cd StocksDashboard
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Next Steps

1. Add GitHub Actions secret for sensitive data
2. Setup Releases/Tags for versioning
3. Create GitHub Pages documentation (optional)
4. Setup branch deployment workflow
5. Add code coverage reporting
