## ⚠️ CRITICAL UPDATE: New GitHub Copilot CLI Required

**BREAKING CHANGE:** The old `gh copilot` extension was deprecated October 25, 2025. This system now uses the **NEW** GitHub Copilot CLI.

### Required Updates

1. **Node.js v22+** - REQUIRED for new Copilot CLI
2. **Fine-grained PAT** - Must have "Copilot Requests" permission  
3. **New CLI Installation** - `npm install -g @github/copilot`
4. **Environment Setup** - Configure `.env` with your token

### Quick Setup

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your fine-grained GitHub token to .env
# GH_TOKEN=github_pat_your_token_here

# 3. Run setup (installs Node.js v22+ Copilot CLI)
chmod +x setup.sh && ./setup.sh
```

See `copilot_CLI_operation.md` for complete migration guide.

---

# YAML-to-Codebase Factory

**A fully automated, production-ready system that turns YAML manifests into finished codebases, validates them, tests them, and ships them automatically.**

## 🎯 What This Does

This repository is a self-contained, headless factory that:

1. **Reads YAML Architecture Manifests** - Single source of truth for entire systems
2. **Auto-generates Documentation** - OpenAPI specs and JSON schemas from manifests  
3. **Validates Everything** - Syntax, schema, and business logic validation
4. **Builds Code Headlessly** - Uses GitHub Copilot CLI to generate production codebases
5. **Tests & Ships Automatically** - Full CI/CD loop with auto-merge on green

## 🏗️ Architecture Overview

```
YAML Manifest → Validation → Doc Generation → Auto-Build → Test → Ship → Deploy
```

### Key Components

- **Architecture Manifests** (`briefs/`) - YAML files describing complete systems
- **Auto-Generated Docs** - OpenAPI contracts and JSON validation schemas  
- **Headless Copilot CLI** - Production code generation without human intervention
- **Automated CI/CD Pipeline** - 6-stage GitHub Actions workflow with auto-healing
- **Multi-Project Support** - Each manifest creates its own `[name]_complete/` directory

## 🚀 Quick Start

### 1. Drop a Manifest

Create `briefs/MyProject_Stack.yaml`:

```yaml
project: MyProject
version: 1.0.0
description: AI-driven platform
components:
  api:
    base_url: https://api.myproject.dev/v1
    endpoints:
      - path: /items
        methods:
          get:
            summary: List items
            response_schema: ItemList
  schemas:
    Item:
      type: object
      properties:
        id: { type: string, format: uuid }
        name: { type: string }
      required: [id, name]
    ItemList:
      type: array
      items: { $ref: "#/components/schemas/Item" }
infrastructure:
  compute: [fastapi]
  databases: [postgres]
```

### 2. Push to Trigger

```bash
git add briefs/MyProject_Stack.yaml
git commit -m "Add MyProject manifest"
git push
```

### 3. Automatic Build Process

- System automatically validates and builds the codebase
- GitHub Copilot CLI generates production code headlessly
- Tests run automatically in CI/CD pipeline
- Auto-merges on green test results
- Creates deployment tags and notifications

### 4. Extract Project

```bash
./tools/export_repo.sh MyProject_complete my-new-repo
```

## 📁 Repository Structure

```text
repo-root/
├── briefs/                          # Architecture manifests (input)
│   └── ToySoldiers_Stack.yaml
├── tools/                           # Local utilities
│   ├── build_docs.py               # Local generator/validator
│   └── export_repo.sh              # Push builds to new repos
├── .github/workflows/               # Automated CI/CD pipeline
│   ├── 00_validate_manifest.yml    # YAML validation
│   ├── 01_generate_docs.yml        # Auto-generate OpenAPI/Schema
│   ├── 02_prepare_confirmation.yml # Auto-approval mechanism
│   ├── 03_production_generate.yml  # Headless Copilot build
│   ├── 04_ship_on_green.yml        # Test & auto-merge
│   └── 05_deploy_complete.yml      # Deployment completion
├── [brief_name]_complete/           # Generated codebases (output)
├── [brief_name]_API_OpenAPI.yaml   # Auto-generated API contracts
├── [brief_name]_API_Schema.json    # Auto-generated validation schemas
└── archive/sample_generations/     # Example inputs/outputs for reference
```

## 🔄 Automated Pipeline Flow

1. **Validation** - Checks YAML syntax and schema compliance
2. **Doc Generation** - Creates OpenAPI and JSON Schema files automatically  
3. **Auto-Approval** - Automatic approval mechanism (no human intervention required)
4. **Production Build** - Copilot CLI generates complete codebase headlessly
5. **Test & Ship** - Runs tests, auto-merges on green, creates issues on red
6. **Deploy Complete** - Final deployment verification and tagging

## 🛠️ Local Development

### Validate & Generate Docs Locally

```bash
pip install pyyaml jsonschema
python tools/build_docs.py
```

### Export Completed Project

```bash
./tools/export_repo.sh ProjectName_complete new-github-repo-name
```

## 🔧 Configuration

### Required GitHub Secrets

- `GITHUB_TOKEN` - Automatically provided by GitHub Actions with proper permissions

### Environment Setup

- GitHub Copilot CLI must be installed and authenticated
- Repository must have GitHub Actions enabled
- All workflows have proper permissions blocks for security compliance

## 🎯 Use Cases

- **Rapid Prototyping** - Manifest to working codebase in minutes
- **Microservices Factory** - Generate consistent service architectures
- **API-First Development** - OpenAPI specs drive implementation
- **Multi-Project Management** - Single repo manages multiple codebases
- **Compliance & Governance** - Enforced patterns and validation

## 🧠 Key Features

### Deterministic Builds

- Same manifest always produces same output
- Full audit trail through GitHub issues and PRs
- Reproducible across environments

### Headless Operation

- No manual intervention required
- Runs in CI/CD without human input
- Fully automated approval workflows

### Multi-Project Support

- Each manifest becomes its own complete project
- Isolated `[name]_complete/` directories
- Easy extraction to standalone repositories

### Auto-Healing Pipeline

- Failed builds automatically trigger regeneration
- Test failures are analyzed and corrected automatically
- Full error context preserved in issue comments and logs

## 📈 Production Ready

This system is battle-tested for:

- ✅ **Headless CI/CD** - No manual steps required
- ✅ **Error Recovery** - Auto-healing on failures  
- ✅ **Multi-tenancy** - Multiple projects in one repo
- ✅ **Audit Compliance** - Full paper trail
- ✅ **Security** - Controlled access via GitHub permissions
- ✅ **Scalability** - Handles dozens of concurrent projects

## 🚨 Important Notes

- Requires GitHub Copilot CLI with headless capabilities
- Manifests must follow the schema defined in validation workflows
- Generated code is automatically committed - review before production deployment
- Each project gets its own complete directory structure
- Full automation pipeline with zero human intervention required

---

**Ready to ship? Drop a manifest in `briefs/` and push!** 🚀