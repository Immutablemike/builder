# Universal Developer Productivity Standards

## Core Development Philosophy

- Leverage GPT-5 native capabilities first - use the power you already have
- Ship working code fast - let GPT-5 handle the complexity
- Smart solutions with native intelligence - no framework overhead
- Direct GPT-5 execution - minimal tool chain, maximum efficiency
- Honest capability assessment - use native features when they're enough
- Keep it powerful but precise - GPT-5 is your primary engine

## Universal Project Standards (GitHub-First)

### Strategic Advantage: GitHub = Universal Cloud Compatibility

When you build to GitHub standards, you get FREE integration with:

- **AWS CodeCommit/CodeBuild** - Reads GitHub Actions workflows directly
- **Google Cloud Build** - Imports GitHub repos with zero friction  
- **Azure DevOps** - Native GitHub integration across all services
- **Vercel/Netlify** - Auto-deploy from GitHub with standard configs
- **Docker Hub** - Automated builds from GitHub repos
- **All CI/CD Platforms** - Support GitHub Actions format universally

### File Format Compliance Standards

#### YAML Files (.yml, .yaml)

```yaml
# ✅ GitHub-compliant YAML
name: Production Deployment
on: [push, workflow_dispatch]
env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.11'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install && npm run build
```

**Standards:**

- **Indentation**: 2 spaces only (never tabs)
- **Line Endings**: Unix LF (`\n`) only  
- **Boolean Values**: `true`/`false` (lowercase)
- **Array Format**: `[item1, item2]` for short lists

#### JSON Files (.json)

```json
{
  "name": "@organization/project-name",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**Standards:**

- **Indentation**: 2 spaces consistently
- **Property Names**: Always quoted with double quotes
- **No Trailing Commas**: Will break parsing
- **Encoding**: UTF-8 without BOM

#### Markdown Files (.md)

**Standards:**

- **Line Endings**: Single trailing newline (MD047)
- **Heading Spacing**: Blank lines around headings (MD022)
- **List Formatting**: Blank lines around lists (MD032)
- **Code Blocks**: Always specify language for syntax highlighting

### Repository Structure Standard

```text
project/
├── README.md                   # GitHub-optimized with badges
├── .env.example               # Security template with all vars
├── .github/
│   ├── workflows/             # CI/CD automation (kebab-case names)
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                      # Documentation structure
│   ├── README.md
│   └── api.md
├── src/                       # Source code
├── tests/                     # Test organization
├── package.json               # Node projects
├── pyproject.toml            # Python projects
├── Dockerfile                # Container definition
└── docker-compose.yml       # Development environment
```

### GitHub Integration Defaults

- **Actions Workflows**: Use latest versions (@v4), kebab-case naming
- **Secrets Management**: Map all .env variables to GitHub Secrets for CI/CD
- **Issue Templates**: Include DRY/KISS/YAGNI constraint validation
- **PR Templates**: Quality gates with auto-merge on compliance
- **Repository Settings**: Auto-delete head branches, squash merge default

## DRY/KISS/YAGNI Principles - Universal Enforcement

### Core Principles

1. **DRY** — Don't Repeat Yourself. One source of truth for logic, schemas, constants.
2. **KISS** — Keep It Simple. Prefer standard library, obvious code, tiny APIs.
3. **YAGNI** — You Aren't Gonna Need It. Only build what the brief demands.
4. **Cohesion & purity**. Small pure functions, explicit I/O, no hidden globals.
5. **Data-first**. Define types/schemas first; code flows from contracts.
6. **Tests guard behavior**. Write with API; bugs = failing test first.
7. **Fail soft**. Actionable errors; no broad catch.
8. **Observability lite**. Minimal structured logs (in/out/errors).
9. **Security by default**. Env config, least privilege, no secrets in code.
10. **Optimize last** (measure before tuning).

### Anti-Over-Engineering Guardrails

**Never Do These Complexity Traps:**

- ❌ Create abstractions with <3 use cases
- ❌ Build frameworks when libraries suffice
- ❌ Add features not explicitly requested
- ❌ Create complex inheritance hierarchies
- ❌ Over-optimize before measuring performance
- ❌ Add middleware/decorators without clear need
- ❌ Create configuration systems for static values

**Always Do These Instead:**

- ✅ Use composition over inheritance
- ✅ Prefer explicit over implicit behavior
- ✅ Choose boring technology that works
- ✅ Build the simplest thing that could work
- ✅ Question every abstraction and dependency

### Non-Negotiable Quality Requirements

- **≤1 new dependency** unless brief explicitly requires more
- **≤40 lines per function**; modules ~200–300 lines maximum
- **≤15 cyclomatic complexity** per function
- **Public API documented** with runnable examples
- **Idempotent operations** - safe to re-run commands/APIs
- **Zero placeholders** - no TODOs, stubs, or dead code
- **Immediate functionality** - all code must work on first run

### Code Quality Checklist

- [ ] DRY: no duplicated logic/constants; shared code centralized
- [ ] KISS: simplest viable approach; no unnecessary abstractions
- [ ] YAGNI: only acceptance criteria implemented
- [ ] **GitHub compliant**: YAML/JSON/MD pass validation
- [ ] **Universal compatibility**: Works across all cloud platforms
- [ ] ≤1 new dependency (documented)
- [ ] Contracts declared + used
- [ ] Tests green (`make test` or `pytest -q`)
- [ ] 30s demo from fresh clone works
- [ ] **Multi-cloud ready**: Standard formats everywhere
- [ ] Actionable errors; no secrets; `.env.example` present
- [ ] Function complexity ≤15

## No Placeholder/Stub Code Enforcement

### Zero Tolerance for Non-Functional Code

**Never Generate:**

- ❌ Placeholder code with TODO comments
- ❌ Stub functions with `pass` or empty implementations
- ❌ "... existing code ..." comments in code blocks
- ❌ Functions that say "implement this later"
- ❌ Incomplete implementations requiring user completion

**Only Acceptable Placeholders:**

- ✅ External API credentials: `API_KEY = "your_api_key_here"`
- ✅ Database connection strings: `DATABASE_URL = "postgresql://localhost/db"`
- ✅ Third-party service tokens: `STRIPE_SECRET_KEY = "sk_test_..."`
- ✅ Environment-specific URLs: `WEBHOOK_URL = "https://your-domain.com/webhook"`

**Enforcement Standards:**

- ✅ ALL code must be immediately executable and functional
- ✅ ALL functions must have complete working implementations
- ✅ ALL examples must be copy-paste ready with minimal setup
- ✅ ALL imports and dependencies must be explicitly specified
- ✅ ALL error handling must be implemented, not stubbed

## Secret & Credential Management

### Environment Variable Standards

- ✅ ALWAYS create .env.example with dummy values for all secrets
- ✅ ALWAYS use environment variables for API keys, database URLs, tokens
- ✅ ALWAYS add .env to .gitignore (never commit real secrets)
- ✅ ALWAYS document required environment variables in README

### GitHub Secrets Integration

- ✅ Map all .env variables to GitHub Secrets for CI/CD
- ✅ Use GITHUB_TOKEN for repository operations when available
- ✅ Implement secret rotation reminders in documentation
- ✅ Validate secret format before usage (API key patterns, URLs, etc.)

### Secret Security Patterns

**Never Do:**

- ❌ Never hardcode API keys, passwords, or tokens in source code
- ❌ Never log secrets in terminal commands or console output
- ❌ Never expose secrets in error messages or debug output

**Always Do:**

- ✅ Use secure environment variable loading (python-dotenv, etc.)
- ✅ Implement secret scanning in pre-commit hooks
- ✅ Rotate secrets regularly and document rotation procedures

## Technology Stack Preferences

### Backend Development

- **Primary API Framework:** FastAPI with automatic OpenAPI documentation
- **Alternative:** Flask for lightweight services
- **Python Version:** Python 3.11+ for optimal performance
- **ASGI Server:** Uvicorn for production deployments
- **Data Validation:** Pydantic v2 for robust data handling

### Database & Persistence

- **Primary Database:** PostgreSQL with async support (asyncpg)
- **ORM:** SQLAlchemy 2.0+ with async capabilities
- **Migrations:** Alembic for database version control
- **Caching:** Redis for session and application caching
- **Object Storage:** MinIO for file storage needs

### Frontend & Mobile

- **Web Applications:** Next.js 14+ with App Router and TypeScript
- **Mobile Applications:** Expo with React Native for cross-platform development
- **Styling:** Tailwind CSS for web, NativeWind for React Native
- **UI Components:** Shadcn/ui for consistent design systems

### Development Tools

- **Code Quality:** Ruff for Python linting and formatting
- **Type Checking:** mypy for Python, built-in for TypeScript
- **Testing:** pytest for Python, Jest for JavaScript/TypeScript
- **Version Control:** Git with conventional commits

### Essential Python Development Environment

```python
# Essential Python packages for modern development
fastapi[all]>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
redis[hiredis]>=5.0.0
httpx>=0.25.0
ruff>=0.1.6
pytest>=7.4.0
```

## Development Workflow

1. **Contracts**: types/schemas + public API + 1–2 usage examples.
2. **Tests**: API shape + 2 happy + 2 edge.
3. **Implement** the smallest slice to go green.
4. **Expose** CLI/HTTP (if in scope).
5. **Docs**: README Quickstart + Example + Config + Limitations.

## Commit/PR Rules

- Commits: small, imperative, one concern.
- PR body: What / Why / How / Limitations.