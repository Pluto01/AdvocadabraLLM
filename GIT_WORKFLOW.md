# Git Workflow Guide for AdvocadabraLLM

## Branch Structure

This project follows a **Git Flow** branching model with the following branches:

### Main Branches
- **`main`** - Production-ready code. Only stable, tested features are merged here.
- **`development`** - Integration branch for features. All feature branches are merged here first.

### Supporting Branches
- **`feature/*`** - New features (e.g., `feature/document-analysis`, `feature/user-auth`)
- **`bugfix/*`** - Bug fixes (e.g., `bugfix/login-error`, `bugfix/api-timeout`)
- **`hotfix/*`** - Critical fixes for production (merged directly to main and development)
- **`release/*`** - Release preparation branches

## Workflow Steps

### 1. Starting New Work

```bash
# Make sure you're on the latest development branch
git checkout development
git pull origin development

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/bug-description
```

### 2. Working on Your Branch

```bash
# Make your changes and commit regularly
git add .
git commit -m "feat: add document upload functionality"

# Push your branch to remote
git push -u origin feature/your-feature-name
```

### 3. Completing Your Work

```bash
# Make sure your branch is up to date with development
git checkout development
git pull origin development
git checkout feature/your-feature-name
git merge development

# Push final changes
git push origin feature/your-feature-name

# Create a Pull Request to merge into development
```

### 4. Release Process

```bash
# Create release branch from development
git checkout development
git pull origin development
git checkout -b release/v1.0.0

# Finalize release (version bumps, final testing)
git commit -m "chore: bump version to v1.0.0"

# Merge to main
git checkout main
git merge release/v1.0.0
git tag v1.0.0

# Merge back to development
git checkout development
git merge release/v1.0.0

# Clean up
git branch -d release/v1.0.0
```

## Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (white-space, formatting)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to build process or auxiliary tools

### Examples:
```bash
git commit -m "feat: add PDF document parsing functionality"
git commit -m "fix: resolve authentication token expiration issue"
git commit -m "docs: update API documentation for legal analysis endpoints"
git commit -m "chore: update dependencies and build scripts"
```

## Current Branch Status

- **`main`**: Stable production code
- **`development`**: Active development branch (current working branch)

## Quick Commands

```bash
# Check current branch and status
git branch -v
git status

# Switch to development branch
git checkout development

# Create new feature branch
git checkout -b feature/your-feature-name

# Sync with remote
git pull origin development

# View branch history
git log --oneline --graph --all
```

## File Management

### Already Configured in .gitignore:
- `node_modules/` (Frontend dependencies)
- `__pycache__/` (Python cache)
- `.env` files (Environment variables)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, etc.)
- Build artifacts (`dist/`, `build/`)

### Important Notes:
- Never commit `node_modules/` or build artifacts
- Always commit `.env.example` but never `.env`
- Keep commits focused and atomic
- Write descriptive commit messages
- Test your code before committing
- Use Pull Requests for code review

## Troubleshooting

### If you accidentally committed node_modules:
```bash
# Unstage the files
git reset HEAD -- node_modules/

# Or remove from history (use carefully)
git rm -r --cached node_modules/
git commit -m "Remove node_modules from tracking"
```

### If branches diverged:
```bash
# Rebase your feature branch onto development
git checkout feature/your-branch
git rebase development
```

### Force push (use with caution):
```bash
# Only use for your own feature branches
git push --force-with-lease origin feature/your-branch
```
