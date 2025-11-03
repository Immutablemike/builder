# GitHub Compliance & Standards Guide

## Universal Standards for All Projects

This document establishes **mandatory compliance standards** for all repositories, files, and code deployed to GitHub and broader cloud services. These standards ensure compatibility, maintainability, and production readiness across all environments.

---

## 🎯 CORE PRINCIPLE: GitHub is the Boss

> **"They are the fucking boss - we adhere to their standards, we work everywhere"**

All files, formats, and structures **MUST** comply with GitHub's standards to ensure:

- ✅ **Universal Compatibility** - Works across all cloud platforms
- ✅ **Production Readiness** - Passes all validation gates
- ✅ **Team Collaboration** - Consistent experience for all developers
- ✅ **CI/CD Reliability** - Automated workflows function correctly

---

## 📁 FILE FORMAT STANDARDS

### YAML Files (.yml, .yaml)

#### YAML Syntax Requirements

```yaml
# ✅ CORRECT - GitHub compliant YAML
name: Production Deployment
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.11'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup environment
        run: |
          echo "Setting up environment"
          echo "NODE_VERSION=${{ env.NODE_VERSION }}" >> $GITHUB_ENV
```

#### YAML Compliance Rules

- **Indentation**: 2 spaces only (never tabs)
- **Line Endings**: Unix LF (`\n`) only
- **Encoding**: UTF-8 without BOM
- **String Quoting**: Use quotes for values with special characters
- **Boolean Values**: `true`/`false` (lowercase)
- **Null Values**: `null` or `~`
- **Comments**: `#` with space after (`# Comment`)
- **Array Format**: Prefer `[item1, item2]` for short lists
- **Multi-line Strings**: Use `|` for literal, `>` for folded

---

### JSON Files (.json)

#### JSON Syntax Requirements

```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Project description",
  "main": "index.js",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write ."
  },
  "dependencies": {
    "typescript": "^5.0.0",
    "react": "^18.2.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/username/repo.git"
  },
  "keywords": ["typescript", "react", "api"],
  "author": "Author Name <email@domain.com>",
  "license": "MIT"
}
```

#### JSON Compliance Rules

- **Indentation**: 2 spaces consistently
- **Property Names**: Always quoted with double quotes
- **String Values**: Double quotes only (no single quotes)
- **Trailing Commas**: Not allowed (will break parsing)
- **Comments**: Not supported (use separate documentation)
- **Encoding**: UTF-8 without BOM
- **Line Endings**: Unix LF (`\n`)

---

### Markdown Files (.md)

### GitHub Flavored Markdown Standards

```markdown
# Project Title

Brief project description with clear value proposition.

## Installation

```bash
# Clone repository
git clone https://github.com/username/repo.git
cd repo

# Install dependencies
npm install
```

## Usage

### Basic Example

```typescript
import { ApiClient } from './api-client';

const client = new ApiClient({
  baseUrl: 'https://api.example.com',
  apiKey: process.env.API_KEY
});

const result = await client.getUser('user-id');
console.log(result);
```

## API Reference

### `getUser(id: string): Promise<User>`

Retrieves user information by ID.

**Parameters:**

- `id` (string): User identifier

**Returns:**

- `Promise<User>`: User object

## License

MIT License - see [LICENSE](LICENSE) file for details.
```markdown

#### Markdown Compliance Rules (GitHub)

- **Line Endings**: Single trailing newline (MD047)
- **Heading Spacing**: Blank lines around headings (MD022)
- **List Formatting**: Blank lines around lists (MD032)
- **Link Format**: Use `[text](url)` format consistently
- **Code Blocks**: Specify language for syntax highlighting
- **Table Format**: Use GitHub table syntax with proper alignment
- **Image Format**: `![alt text](url "optional title")`
- **Emoji Support**: Use GitHub emoji shortcodes (`:tada:`)

---

## 🐍 PYTHON STANDARDS

### Project Structure

```text
project-name/
├── README.md
├── pyproject.toml              # Modern Python packaging
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── .env.example               # Environment template
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── src/
│   └── project_name/          # Package directory
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       ├── core/
│       ├── models/
│       └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py
└── docs/
    ├── README.md
    └── api.md
```

### pyproject.toml Standards

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "project-name"
version = "1.0.0"
description = "Project description"
readme = "README.md"
license = { file = "LICENSE" }
authors = [
    { name = "Author Name", email = "author@example.com" }
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "sqlalchemy[asyncio]>=2.0.0",
]
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501", "F401"]

[tool.black]
target-version = ["py311"]
line-length = 88

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

---

## 📱 TYPESCRIPT/JAVASCRIPT STANDARDS

### Project Structure

```text
project-name/
├── README.md
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── src/
│   ├── index.ts
│   ├── types/
│   ├── components/
│   ├── services/
│   ├── utils/
│   └── __tests__/
├── dist/                      # Build output
├── docs/
└── examples/
```

### package.json Standards

```json
{
  "name": "@organization/project-name",
  "version": "1.0.0",
  "description": "TypeScript project with modern tooling",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ],
  "scripts": {
    "build": "tsc",
    "dev": "tsx watch src/index.ts",
    "test": "jest",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "typescript": "^5.3.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/organization/project-name.git"
  },
  "keywords": ["typescript", "api", "sdk"],
  "author": "Author Name <email@example.com>",
  "license": "MIT"
}
```

---

## 🐳 DOCKER STANDARDS

### Dockerfile Standards

```dockerfile
# syntax=docker/dockerfile:1.7-labs
FROM node:18-alpine AS base

# Install security updates
RUN apk update && apk upgrade && \
    apk add --no-cache \
    dumb-init \
    curl \
    && rm -rf /var/cache/apk/*

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Dependencies stage
FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Build stage
FROM base AS builder
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json

# Security: use non-root user
USER nextjs

EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

---

## 🔧 MAKEFILE STANDARDS

### Essential Makefile Structure

```makefile
# Project Configuration
PROJECT_NAME := project-name
VERSION := $(shell git describe --tags --always --dirty)

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
NC := \033[0m # No Color

.PHONY: help install dev build test clean

# Default target
.DEFAULT_GOAL := help

## Display this help message
help:
    @echo "$(BLUE)$(PROJECT_NAME) - Development Commands$(NC)"
    @echo ""
    @awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## Install dependencies
install:
    @echo "$(BLUE)Installing dependencies...$(NC)"
    npm ci
    @echo "$(GREEN)Dependencies installed$(NC)"

## Start development server
dev:
    @echo "$(BLUE)Starting development server...$(NC)"
    npm run dev

## Build for production
build:
    @echo "$(BLUE)Building for production...$(NC)"
    npm run build
    @echo "$(GREEN)Build complete$(NC)"

## Run tests
test:
    @echo "$(BLUE)Running tests...$(NC)"
    npm test

## Clean build artifacts
clean:
    @echo "$(BLUE)Cleaning build artifacts...$(NC)"
    rm -rf dist node_modules/.cache
    @echo "$(GREEN)Clean complete$(NC)"
```

---

## 🚀 REPOSITORY STRUCTURE STANDARDS

### Universal Repository Template

```text
project-name/
├── README.md                          # GitHub-optimized documentation
├── LICENSE                            # Open source license
├── .gitignore                         # Comprehensive ignore patterns
├── .env.example                       # Environment template
├── package.json                       # Node.js projects
├── pyproject.toml                     # Python projects
├── Dockerfile                         # Container definition
├── docker-compose.yml                 # Development environment
├── Makefile                          # Development automation
├── .github/                          # GitHub automation
│   ├── workflows/                    # GitHub Actions
│   │   ├── ci.yml                   # Continuous integration
│   │   ├── deploy.yml               # Deployment pipeline
│   │   └── security.yml             # Security scanning
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md     # PR template
│   └── CODEOWNERS                   # Code ownership
├── docs/                            # Documentation
│   ├── README.md                    # Documentation index
│   ├── api.md                       # API documentation
│   └── deployment.md                # Deployment guide
├── src/                             # Source code
│   ├── index.ts                     # Entry point
│   ├── types/                       # Type definitions
│   ├── services/                    # Business logic
│   ├── utils/                       # Utilities
│   └── __tests__/                   # Tests
├── tests/                           # Additional tests
│   ├── integration/                 # Integration tests
│   ├── e2e/                        # End-to-end tests
│   └── fixtures/                   # Test data
├── scripts/                         # Build/deployment scripts
│   ├── setup.sh                    # Development setup
│   ├── build.sh                    # Build script
│   └── deploy.sh                   # Deployment script
└── examples/                        # Usage examples
    ├── basic.ts                     # Basic usage
    └── advanced.ts                  # Advanced usage
```

---

## 🛡️ SECURITY STANDARDS

### Environment Variables

```bash
# .env.example - Template for environment configuration
# Copy to .env and fill in actual values

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/database
REDIS_URL=redis://localhost:6379

# API Keys (never commit actual values)
API_KEY=your_api_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_key
JWT_SECRET=your_jwt_secret_minimum_32_chars

# Service URLs
BASE_URL=http://localhost:3000
WEBHOOK_URL=https://your-domain.com/webhook

# Feature Flags
ENABLE_ANALYTICS=true
DEBUG_MODE=false
```

### .gitignore Standards

```gitignore
# Environment variables
.env
.env.local
.env.production
.env.staging

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Build outputs
dist/
build/
*.tsbuildinfo
.next/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
*.log

# Testing
coverage/
.nyc_output/
.pytest_cache/

# Temporary files
*.tmp
*.temp
.cache/

# Security
*.pem
*.key
*.crt
secrets.json
```

---

## 📋 QUALITY CHECKLIST

### Pre-Commit Requirements

- [ ] **YAML files** pass syntax validation
- [ ] **JSON files** are valid and properly formatted
- [ ] **Markdown files** follow GitHub formatting standards
- [ ] **Environment files** have corresponding .example templates
- [ ] **Docker files** use multi-stage builds and security best practices
- [ ] **Makefiles** include all standard targets
- [ ] **README.md** includes installation, usage, and contributing sections
- [ ] **GitHub Actions** use latest action versions
- [ ] **All files** have Unix line endings (LF)
- [ ] **No secrets** are committed to repository

### Production Readiness

- [ ] **Health checks** implemented for all services
- [ ] **Monitoring** and alerting configured
- [ ] **Security scanning** automated in CI/CD
- [ ] **Performance testing** included in pipeline
- [ ] **Documentation** complete and up-to-date
- [ ] **Error handling** comprehensive and user-friendly
- [ ] **Logging** structured and appropriate for production
- [ ] **Dependencies** pinned to specific versions
- [ ] **Backup and recovery** procedures documented
- [ ] **Load testing** validates performance requirements

---

## 🎯 STANDARDIZATION OPPORTUNITIES

### Across All Your Projects

1. **GitHub Actions Templates**
   - Create organization-level workflow templates
   - Standardize CI/CD pipeline structure
   - Implement universal security scanning

2. **Repository Templates**
   - Organization template repository with complete structure
   - Automated setup scripts for new projects
   - Consistent documentation patterns

3. **Development Tools**
   - Shared ESLint/Prettier configurations
   - Universal Makefile targets
   - Standard Docker configurations

4. **Quality Gates**
   - Mandatory code coverage thresholds
   - Security scanning requirements
   - Performance benchmarking standards

### Implementation Strategy

#### Create Organization Standards Repository

```text
standards/
├── templates/
│   ├── repository/           # Complete repo template
│   ├── workflows/           # GitHub Actions templates
│   ├── configs/             # Tool configurations
│   └── docs/               # Documentation templates
├── tools/
│   ├── setup-repo.sh        # Repository setup automation
│   ├── validate-compliance.sh # Compliance checking
│   └── migrate-project.sh   # Migrate existing projects
└── docs/
    ├── github_compliance.md # This document
    ├── architecture_guide.md
    └── security_guide.md
```

#### Automated Compliance Checking

- Pre-commit hooks for format validation
- CI/CD pipeline compliance verification
- Regular audits of existing repositories

#### Migration Plan

- Assess current projects against standards
- Prioritize high-impact compliance fixes
- Gradual migration with backwards compatibility

**This universal standard ensures all your projects work seamlessly across GitHub and cloud platforms, maintaining production readiness and team productivity.**
