# Operating Room Surgery Instructions

## Raw Chat Processing & Project Extraction Protocol

**Purpose**: Transform raw ChatGPT conversation exports (YAML files) into structured project directories containing build briefs and extracted documentation.

**Output**: Clean project directory in `Operating_Room/[Project_Name]/` with build brief ready for Builder/briefs/ workflow.

---

## 🎯 **SURGICAL OBJECTIVE**

### Primary Output Structure

```text
Operating_Room/[Project_Name]/
├── [Project_Name]_build_brief.yaml   # → Copy to Builder/briefs/ when ready
├── docs/                         # Extracted documentation
│   ├── README.md
│   ├── Repository_Structure.md
│   ├── API_Documentation.md
│   ├── Database_Schema.md
│   └── Architecture_Overview.md
├── schemas/                      # API/DB schemas if found
│   ├── openapi.yaml
│   └── database.sql
└── .extracted_metadata.json     # Surgery tracking data
```

### Workflow Integration

1. **Drop raw chat YAML** → `Operating_Room/[Project]_Raw_Chat.yaml`
2. **Surgery extracts** → `Operating_Room/[Project_Name]/` directory
3. **Manual review** → Validate [Project_Name]_build_brief.yaml and docs
4. **Deploy brief** → `cp [Project_Name]/[Project_Name]_build_brief.yaml briefs/`
5. **Generate project** → `make generate-project BRIEF=briefs/[Project_Name]_build_brief.yaml`

---

## 🚨 CRITICAL - Pre-Surgery Assessment

### Before Processing Any Raw Material

1. **Identify the Raw Material Type**

   **Raw Chat Files:**
   - Files typically end in `_Raw_Chat.yaml`
   - Located in `/Operating_Room/` directory
   - Contains unstructured conversational content

   **XML Project Briefs:**
   - Files typically end in `_Project_Brief.xml` or `_Brief.xml`
   - Located in `/Operating_Room/` directory
   - Contains structured project specifications (like Human_Atlas_Project_Brief.xml)

2. **Scan for Project Intent**
   - Look for project names, goals, and scope statements
   - Identify technology stack decisions
   - Extract business requirements and user stories

3. **Inventory Technical Artifacts**
   - API specifications and endpoint definitions
   - Database schemas and table structures
   - Architecture diagrams and system topology
   - Configuration files and environment setups

---

## 🔍 SURGICAL EXTRACTION PROCESS

### Phase 1 - Project Discovery & Analysis

#### Initial Raw Chat Assessment

```bash
# Read the raw chat file
read_file("/Users/michaelsprimary/builder/Operating_Room/[PROJECT]_Raw_Chat.yaml")

# Discover project fundamentals
semantic_search("project name description goals objectives")
semantic_search("technology stack frameworks architecture")
semantic_search("repository structure monorepo services")
```

#### Extract Core Project DNA

**Primary Extraction Targets:**

- **Project Name & Description** - For build_brief.yaml header
- **Technology Stack** - Backend/frontend framework decisions  
- **Repository Structure** - Monorepo layout and service organization
- **API Contracts** - Endpoint definitions and data models
- **Database Schema** - Table structures and relationships
- **Infrastructure** - Deployment and hosting requirements
- **Environment Config** - Required variables and secrets

### Phase 2 - Build Brief Construction

#### Create build_brief.yaml Structure

Based on ToySoldiers_Stack.yaml pattern, extract and structure:

```yaml
project_meta:
  name: "[Extracted Project Name]"
  description: "[Extracted Description]"
  owner: "[Extracted Owner/Organization]"
  repo_structure: "[monorepo|single|microservices]"
  deployment_strategy: "[cloud|hybrid|on-premise]"

environments:
  development: "[Local development setup]"
  staging: "[Staging environment config]"
  production: "[Production deployment target]"

repo_tree: |
  [Extracted repository structure tree]

backend_services: "[Extracted service definitions]"
frontend_services: "[Extracted frontend architecture]"
infrastructure: "[Extracted infrastructure requirements]"
```

### Phase 3 - Documentation Extraction

#### Extract Supplementary Documents

##### Repository Structure Document

```bash
# Find repository/directory structures
grep_search("├──|└──|repo|directory|folder|structure|tree", isRegexp=true)
```

##### API Documentation

```bash
# Find API endpoint definitions
grep_search("POST|GET|PUT|DELETE|/api/|endpoints|routes", isRegexp=true)
```

##### Database Schema

```bash
# Find database/table definitions
grep_search("tables|CREATE TABLE|schema|database|models", isRegexp=true)
```

##### Architecture Overview

```bash
# Find system architecture discussions
semantic_search("architecture microservices monorepo system design")
```

---

## � **COMPLETE SURGICAL WORKFLOW**

### Step 1 - Prepare Operating Theater

```bash
# Navigate to Operating Room
cd /Users/michaelsprimary/builder/Operating_Room/

# Identify raw chat file
ls -la *_Raw_Chat.yaml

# Extract project name from filename
PROJECT_NAME=$(basename *_Raw_Chat.yaml _Raw_Chat.yaml)
echo "Operating on: $PROJECT_NAME"
```

### Step 2 - Initial Assessment & Discovery

```bash
# Read the raw material
read_file("Operating_Room/${PROJECT_NAME}_Raw_Chat.yaml")

# Discover project fundamentals
semantic_search("project name description goals technology stack")
semantic_search("repository structure monorepo architecture services")
semantic_search("database schema API endpoints infrastructure")
```

### Step 3 - Extract Build Brief

Create `Operating_Room/${PROJECT_NAME}/${PROJECT_NAME}_build_brief.yaml` following ToySoldiers_Stack.yaml pattern:

```yaml
# Based on extracted content, create comprehensive build brief
project_meta:
  name: "[EXTRACTED_NAME]"
  description: "[EXTRACTED_DESCRIPTION]" 
  owner: "[EXTRACTED_OWNER]"
  repo_structure: "[EXTRACTED_STRUCTURE_TYPE]"
  deployment_strategy: "[EXTRACTED_DEPLOYMENT]"

# Continue with full ToySoldiers_Stack.yaml structure...
```

### Step 4 - Extract Documentation

Create supporting documents in `Operating_Room/${PROJECT_NAME}/docs/`:

- **README.md** - Project overview and quick start
- **Repository_Structure.md** - Extracted repo tree and organization
- **API_Documentation.md** - Endpoint definitions and contracts
- **Database_Schema.md** - Table structures and relationships
- **Architecture_Overview.md** - System design and service layout

### Step 5 - Quality Validation

```bash
# Validate build brief YAML syntax
python3 -c "import yaml; yaml.safe_load(open('${PROJECT_NAME}/${PROJECT_NAME}_build_brief.yaml'))"

# Check GitHub compliance on all docs
get_errors(["${PROJECT_NAME}/docs/*.md"])

# Verify no placeholder content remains
grep -r "TODO\|PLACEHOLDER\|FIXME" ${PROJECT_NAME}/
```

### Step 6 - Surgery Completion

```bash
# Create surgery metadata
cat > ${PROJECT_NAME}/.extracted_metadata.json << EOF
{
  "surgery_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "raw_chat_file": "${PROJECT_NAME}_Raw_Chat.yaml",
  "extracted_documents": [
    "[PROJECT_NAME]_build_brief.yaml",
    "docs/README.md",
    "docs/Repository_Structure.md",
    "docs/API_Documentation.md",
    "docs/Database_Schema.md",
    "docs/Architecture_Overview.md"
  ],
  "ready_for_builder": true
}
EOF

# Success confirmation
echo "✅ Surgery complete: Operating_Room/${PROJECT_NAME}/"
echo "📋 Next: cp ${PROJECT_NAME}/${PROJECT_NAME}_build_brief.yaml briefs/"
echo "🚀 Then: make generate-project BRIEF=briefs/${PROJECT_NAME}_build_brief.yaml"
```

---

## 🔄 **XML PROJECT BRIEF CONVERSION PROTOCOL**

### Purpose: Transform XML Project Briefs to YAML Build Briefs

**Input**: Comprehensive XML project specifications (like Human_Atlas_Project_Brief.xml)
**Output**: Builder-compatible YAML build brief + extracted documentation

### XML-to-YAML Conversion Workflow

#### Step 1 - XML Assessment & Parsing

```bash
# Read the XML project brief
read_file("/Users/michaelsprimary/builder/Operating_Room/[PROJECT]_Project_Brief.xml")

# Parse XML structure and identify key sections
grep_search("<ProjectMeta>|<Mission>|<Scope>|<Architecture>|<DataStructures>|<Economics>", isRegexp=true)
```

#### Step 2 - Extract Core Project Metadata

**From `<ProjectMeta>` section extract:**

```yaml
project_meta:
  name: "[From <ProjectName>]"
  version: "[From <Version>]"
  description: "[From <Summary>]"
  owner: "[From <PrimaryArchitect> / <Governance>]"
  classification: "[From <Classification>]"
  core_mission: "[From <CoreMission>]"
```

#### Step 3 - Transform Architecture Section

**From `<Architecture>` → `<Services>` extract:**

```yaml
backend_services:
  api_gateway:
    framework: "[From Framework field]"
    endpoints: "[From Endpoints list]"
    security: "[From Security field]"
  
  # Transform each <Service> into service definition
  [service_name]:
    stack: "[From Stack field]"
    function: "[From Function field]"
    runtime: "[From Runtime field]"
```

#### Step 4 - Transform Data Structures

**From `<DataStructures>` extract:**

```yaml
database_schemas:
  # From <RelationalSchema>
  postgres:
    tables:
      # Transform each <Table> into schema definition
      [table_name]:
        description: "[From Description]"
        fields: "[From Fields, parsed into key-value]"
        
  # From <VectorSchema>  
  qdrant:
    collections:
      [collection_name]:
        vector_size: "[From VectorSize]"
        distance_metric: "[From DistanceMetric]"
```

#### Step 5 - Transform Infrastructure

**From `<Infrastructure>` extract:**

```yaml
infrastructure:
  containerization:
    orchestrator: "[From Orchestrator]"
    containers: "[From Containers list]"
  networks: "[From Networks]"
  storage: "[From Storage]"
```

#### Step 6 - Create Repository Structure

**From `<Appendices>` → `<RepositoryStructure>` extract:**

```yaml
repo_tree: |
  [Transform <Tree> section into clean directory structure]
```

### Complete XML-to-YAML Conversion Template

```yaml
# Generated from [XML_FILENAME] on [DATE]
project_meta:
  name: "[EXTRACTED_PROJECT_NAME]"
  version: "[EXTRACTED_VERSION]"
  description: "[EXTRACTED_DESCRIPTION]"
  owner: "[EXTRACTED_OWNER]"
  repo_structure: "monorepo"  # Usually inferred from XML complexity
  deployment_strategy: "[EXTRACTED_FROM_INFRA]"

environments:
  development:
    description: "Local development with Docker Compose"
    compose_file: "docker-compose.yml"
  staging:
    description: "[EXTRACTED_OR_INFERRED]"
  production:
    description: "[EXTRACTED_FROM_DEPLOYMENT_NOTES]"

repo_tree: |
  [EXTRACTED_REPOSITORY_STRUCTURE]

backend_services:
  [CONVERTED_FROM_ARCHITECTURE_SERVICES]

frontend_services:
  [CONVERTED_FROM_FRONTEND_COMPONENTS]

infrastructure:
  [CONVERTED_FROM_INFRASTRUCTURE_SECTION]

database_schemas:
  [CONVERTED_FROM_DATA_STRUCTURES]

api_contracts:
  [CONVERTED_FROM_ENDPOINTS_DEFINITIONS]

environment_variables:
  [CONVERTED_FROM_ENVIRONMENT_VARIABLES_SECTION]

economics:
  [CONVERTED_FROM_ECONOMICS_SECTION_IF_EXISTS]

governance:
  [CONVERTED_FROM_GOVERNANCE_SECTION_IF_EXISTS]
```

### XML Conversion Extraction Commands

#### Parse Project Metadata

```bash
# Extract project name
grep_search("<ProjectName>.*</ProjectName>", isRegexp=true)

# Extract description/summary  
grep_search("<Summary>.*</Summary>", isRegexp=true)

# Extract version
grep_search("<Version>.*</Version>", isRegexp=true)
```

#### Parse Services Architecture

```bash
# Find all service definitions
grep_search("<Service name=", isRegexp=true)

# Extract service details
semantic_search("Framework Stack Function Runtime endpoints security")
```

#### Parse Database Schemas

```bash
# Find table definitions
grep_search("<Table name=", isRegexp=true)

# Extract field definitions
grep_search("<Fields>.*</Fields>", isRegexp=true)
```

#### Parse Infrastructure

```bash
# Find containerization setup
grep_search("<Containerization>|<Containers>|<Networks>", isRegexp=true)

# Extract deployment configuration
semantic_search("Docker Compose kubernetes deployment hosting")
```

### XML-Specific Documentation Extraction

#### From `<Governance>` Section

Create `docs/Governance_Framework.md`:

```markdown
# Governance Framework

## Consent Management
[Extract from <ConsentFramework>]

## Privacy & Security
[Extract from <PrivacyAndSecurity>]

## Bias Monitoring
[Extract from <BiasAndFairness>]

## Audit & Compliance
[Extract from <AuditAndLogging>]
```

#### From `<Economics>` Section

Create `docs/Business_Model.md`:

```markdown
# Business Model & Economics

## Compensation Model
[Extract from <CompensationModel>]

## Payment Infrastructure
[Extract from <PaymentInfrastructure>]

## Data Valuation
[Extract from <DataValuationEngine>]

## Marketplace Integration
[Extract from <MarketplaceIntegration>]
```

#### From `<DataStructures>` Section

Create `docs/Database_Schema.md`:

```markdown
# Database Schema Documentation

## Relational Schema (PostgreSQL)
[Extract and format all <Table> definitions]

## Vector Database (Qdrant)
[Extract <Collections> definitions]

## Object Storage Structure
[Extract <ObjectStorage> bucket definitions]
```

### XML Conversion Quality Gates

#### Structural Validation

- [ ] **All major XML sections converted to YAML equivalents**
- [ ] **Repository structure accurately reflects XML `<Tree>` section**
- [ ] **All services from `<Architecture>` → `<Services>` included**
- [ ] **Database schemas preserve field definitions and relationships**
- [ ] **Infrastructure setup matches `<Infrastructure>` specifications**

#### Content Completeness

- [ ] **No `<CDATA>` sections lost in conversion**
- [ ] **Environment variables from `<EnvironmentVariables>` preserved**
- [ ] **DAG orchestration logic captured if present**
- [ ] **Monitoring and observability requirements preserved**
- [ ] **Security specifications maintained**

#### YAML Compliance

- [ ] **Valid YAML syntax (no conversion errors)**
- [ ] **Follows ToySoldiers_Stack.yaml structural pattern**
- [ ] **All string values properly quoted/escaped**
- [ ] **Lists and objects correctly formatted**
- [ ] **No XML artifacts (tags, attributes) in final YAML**

### Post-Conversion Integration

#### Deploy Converted Brief

```bash
# Copy converted YAML to briefs directory
cp ${PROJECT_NAME}/${PROJECT_NAME}_build_brief.yaml ../briefs/

# Validate YAML structure
python3 -c "import yaml; yaml.safe_load(open('../briefs/${PROJECT_NAME}_build_brief.yaml'))"

# Test with builder workflow
cd .. && make generate-project BRIEF=briefs/${PROJECT_NAME}_build_brief.yaml
```

#### Merge Extracted Documentation

```bash
# Copy XML-specific docs to generated project
cp -r Operating_Room/${PROJECT_NAME}/docs/* ${PROJECT_NAME}_complete/docs/

# Ensure all documentation cross-references are updated
# Update README.md to include governance and business model docs
```

---

## 🎯 **INTEGRATION WITH BUILDER WORKFLOW**

### Manual Handoff Process

#### For Raw Chat Files

1. **Review Surgery Output**

   ```bash
   cd Operating_Room/${PROJECT_NAME}
   cat ${PROJECT_NAME}_build_brief.yaml   # Validate build brief
   ls docs/                               # Check extracted docs
   ```

#### For XML Project Briefs  

1. **Review XML Conversion Output**

   ```bash
   cd Operating_Room/${PROJECT_NAME}
   cat ${PROJECT_NAME}_build_brief.yaml   # Validate converted YAML
   ls docs/                               # Check extracted docs (including Governance, Economics)
   python3 -c "import yaml; yaml.safe_load(open('${PROJECT_NAME}_build_brief.yaml'))"  # YAML syntax check
   ```

#### Universal Deployment Steps

1. **Deploy to Builder**

   ```bash
   cp ${PROJECT_NAME}_build_brief.yaml ../briefs/
   cd ..
   make list-briefs                       # Confirm brief is available
   ```

2. **Generate Complete Project**

   ```bash
   make generate-project BRIEF=briefs/${PROJECT_NAME}_build_brief.yaml
   ```

3. **Merge Documentation**

   ```bash
   # Merge extracted docs with generated project
   cp -r Operating_Room/${PROJECT_NAME}/docs/* ${PROJECT_NAME}_complete/docs/
   ```

### Material Type Detection & Routing

#### Automatic Processing Selection

```bash
# Determine input type and route to appropriate process
if [[ $FILENAME == *"_Raw_Chat.yaml" ]]; then
    echo "🗣️  Processing Raw Chat File"
    # Follow Raw Chat Surgical Extraction Process
elif [[ $FILENAME == *"_Project_Brief.xml" ]] || [[ $FILENAME == *"_Brief.xml" ]]; then
    echo "📋 Processing XML Project Brief"
    # Follow XML-to-YAML Conversion Protocol
else
    echo "❌ Unknown file type: $FILENAME"
    echo "Supported: *_Raw_Chat.yaml, *_Project_Brief.xml, *_Brief.xml"
    exit 1
fi
```

### Automated Future Enhancement

Could create `make operate PROJECT=name` that:

#### Raw Chat Processing

- Runs complete surgery on `Operating_Room/${PROJECT}_Raw_Chat.yaml`
- Auto-deploys build brief to `briefs/`
- Triggers project generation
- Merges extracted docs with generated structure

#### XML Project Brief Processing

- Runs XML-to-YAML conversion on `Operating_Room/${PROJECT}_Project_Brief.xml`
- Validates YAML syntax and structure
- Auto-deploys converted brief to `briefs/`
- Triggers project generation with specialized documentation merge

### GitHub Compliance Requirements

#### Markdown Standards (Per github_compliance.md)

- **Line Endings**: Unix LF (`\n`) only
- **Indentation**: 2 spaces for lists, 4 spaces for code blocks
- **Code Blocks**: Always specify language (`python`, `yaml`, `bash`)
- **Headings**: Blank lines before and after (MD022)
- **Lists**: Blank lines around lists (MD032)
- **Final Newline**: Single trailing newline (MD047)

#### File Structure Standards

```text
project-name/
├── README.md                   # Project overview
├── docs/                      # Documentation directory
│   ├── Repository_Structure.md
│   ├── API_Documentation.md
│   ├── Database_Schema.md
│   ├── Architecture_Overview.md
│   ├── Deployment_Guide.md
│   ├── Environment_Setup.md
│   └── Development_Workflow.md
├── .env.example               # Environment template
├── .gitignore                 # Standard ignore patterns
└── package.json               # Dependencies and scripts
```

### Content Organization Principles

#### 1. Start with Executive Summary

Every document begins with:

- **Purpose**: What this document covers
- **Scope**: What's included/excluded
- **Prerequisites**: What reader needs to know
- **Quick Start**: Fastest path to value

#### 2. Use Progressive Disclosure

- High-level overview first
- Detailed implementation second
- Reference materials last

#### 3. Include Working Examples

- All code examples must be functional
- Provide complete, copy-paste ready snippets
- Include expected outputs and error handling

#### 4. Maintain Consistency

- Use same terminology throughout
- Consistent file naming conventions
- Standard section ordering across documents

---

## 🤖 **AGENT EXECUTION INSTRUCTIONS**

### For Future AI Agents Processing XML Project Briefs

#### AGENT PROTOCOL: Execute Complete XML-to-YAML Conversion

```bash
# STEP 1: Identify and validate XML input
FILENAME=$(ls /Users/michaelsprimary/builder/Operating_Room/*_Project_Brief.xml | head -1)
if [ -z "$FILENAME" ]; then
    echo "❌ No XML project brief found"
    exit 1
fi

PROJECT_NAME=$(basename "$FILENAME" _Project_Brief.xml)
echo "🔄 Processing XML Project Brief: $PROJECT_NAME"

# STEP 2: Create project directory
mkdir -p "Operating_Room/${PROJECT_NAME}"
cd "Operating_Room/${PROJECT_NAME}"

# STEP 3: Execute systematic XML-to-YAML conversion
echo "📋 Executing XML-to-YAML conversion protocol..."
```

#### AGENT EXTRACTION COMMANDS

**Execute these commands in sequence:**

```bash
# Read XML content
read_file("$FILENAME")

# Parse project metadata with semantic search
semantic_search("ProjectName Summary Version Classification CoreMission PrimaryArchitect")

# Extract architecture components
grep_search("<Service name=|<Framework>|<Stack>|<Function>", isRegexp=true)

# Extract database schemas
grep_search("<Table name=|<Fields>|<Description>", isRegexp=true)

# Extract infrastructure definitions
grep_search("<Orchestrator>|<Networks>|<Storage>|<Containers>", isRegexp=true)

# Extract repository structure
grep_search("<Tree>|<RepositoryStructure>", isRegexp=true)

# Extract governance and economics (if present)
semantic_search("ConsentFramework PrivacyAndSecurity BiasAndFairness CompensationModel")
```

#### AGENT YAML GENERATION PROTOCOL

**Create `${PROJECT_NAME}_build_brief.yaml` with this structure:**

```yaml
# Template for agent to populate
project_meta:
  name: "[EXTRACT_FROM_ProjectName]"
  version: "[EXTRACT_FROM_Version]"
  description: "[EXTRACT_FROM_Summary]"
  owner: "[EXTRACT_FROM_PrimaryArchitect]"
  classification: "[EXTRACT_FROM_Classification]"
  core_mission: "[EXTRACT_FROM_CoreMission]"
  repo_structure: "monorepo"
  deployment_strategy: "[INFER_FROM_Infrastructure]"

environments:
  development:
    description: "Local development with Docker Compose"
    compose_file: "docker-compose.yml"
  staging:
    description: "[EXTRACT_OR_INFER_FROM_XML]"
  production:
    description: "[EXTRACT_FROM_Deployment_OR_Infrastructure]"

repo_tree: |
  [TRANSFORM_Tree_Section_To_Clean_Structure]

backend_services:
  [CONVERT_ALL_Service_Definitions_From_Architecture]

frontend_services:
  [EXTRACT_Frontend_Components_From_Architecture]

infrastructure:
  [CONVERT_Infrastructure_Section_Complete]

database_schemas:
  [CONVERT_ALL_DataStructures_Schemas]

api_contracts:
  [EXTRACT_Endpoint_Definitions_And_Create_OpenAPI_Structure]

environment_variables:
  [EXTRACT_OR_INFER_Required_Environment_Variables]

# XML-specific sections (if present)
economics:
  [CONVERT_Economics_Section_If_Exists]

governance:
  [CONVERT_Governance_Section_If_Exists]
```

#### AGENT DOCUMENTATION GENERATION

**Create specialized documentation files:**

```bash
# Create docs directory
mkdir -p docs

# Generate comprehensive documentation
create_file("docs/README.md", "[PROJECT_OVERVIEW_FROM_SUMMARY]")
create_file("docs/Architecture_Overview.md", "[CONVERT_Architecture_Section]")
create_file("docs/Database_Schema.md", "[CONVERT_DataStructures_Section]")
create_file("docs/API_Documentation.md", "[CONVERT_Endpoints_TO_API_DOCS]")

# Generate XML-specific docs (if sections exist)
if grep -q "<Governance>" "$FILENAME"; then
    create_file("docs/Governance_Framework.md", "[CONVERT_Governance_Section]")
fi

if grep -q "<Economics>" "$FILENAME"; then
    create_file("docs/Business_Model.md", "[CONVERT_Economics_Section]")
fi
```

#### AGENT VALIDATION PROTOCOL

**Execute quality gates:**

```bash
# Validate YAML syntax
python3 -c "
import yaml
try:
    with open('${PROJECT_NAME}_build_brief.yaml', 'r') as f:
        yaml.safe_load(f)
    print('✅ YAML syntax valid')
except Exception as e:
    print(f'❌ YAML syntax error: {e}')
    exit(1)
"

# Validate required sections exist
REQUIRED_SECTIONS=("project_meta" "backend_services" "infrastructure" "database_schemas")
for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "^${section}:" "${PROJECT_NAME}_build_brief.yaml"; then
        echo "✅ Required section: $section"
    else
        echo "❌ Missing required section: $section"
        exit 1
    fi
done

# Validate documentation files created
DOC_FILES=("docs/README.md" "docs/Architecture_Overview.md" "docs/Database_Schema.md")
for doc in "${DOC_FILES[@]}"; do
    if [[ -f "$doc" ]]; then
        echo "✅ Documentation created: $doc"
    else
        echo "❌ Missing documentation: $doc"
        exit 1
    fi
done
```

#### AGENT COMPLETION PROTOCOL

```bash
# Create surgery metadata
cat > ".extracted_metadata.json" << EOF
{
  "surgery_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "source_type": "XML_Project_Brief",
  "source_file": "${FILENAME}",
  "extracted_documents": [
    "${PROJECT_NAME}_build_brief.yaml",
    "docs/README.md",
    "docs/Architecture_Overview.md", 
    "docs/Database_Schema.md",
    "docs/API_Documentation.md"
  ],
  "xml_specific_docs": [
    "docs/Governance_Framework.md",
    "docs/Business_Model.md"
  ],
  "ready_for_builder": true,
  "validation_passed": true
}
EOF

# Final success confirmation
echo "✅ XML-to-YAML conversion complete: Operating_Room/${PROJECT_NAME}/"
echo "📋 Next: cp ${PROJECT_NAME}/${PROJECT_NAME}_build_brief.yaml ../briefs/"
echo "🚀 Then: make generate-project BRIEF=briefs/${PROJECT_NAME}_build_brief.yaml"
```

#### AGENT ERROR HANDLING

```bash
# If conversion fails at any step
if [[ $? -ne 0 ]]; then
    echo "❌ XML conversion failed at step: [CURRENT_STEP]"
    echo "📝 Logging error to ISSUES.md"
    
    cat > "CONVERSION_ERROR.md" << EOF
# XML Conversion Error Report

**Date**: $(date)
**Source**: $FILENAME  
**Project**: $PROJECT_NAME
**Failed Step**: [CURRENT_STEP]
**Error**: [ERROR_DETAILS]

## Recovery Actions Required:
1. Manual review of XML structure
2. Validate XML sections match expected format
3. Check for non-standard XML formatting
4. Review extraction commands for compatibility

## XML Structure Analysis:
[PASTE_XML_STRUCTURE_ANALYSIS]
EOF
    
    exit 1
fi
```

### For Raw Chat Processing (Existing Protocol)

Agent execution follows existing surgical workflow in sections above

---

## 🔧 EXTRACTION WORKFLOW

### Step-by-Step Process

#### 1. Initial Assessment

```bash
# Read the raw chat file
read_file("/Users/michaelsprimary/builder/Operating_Room/[PROJECT]_Raw_Chat.yaml")

# Identify project scope and boundaries
semantic_search("project name description goals objectives")
```

#### 2. Technical Inventory

```bash
# Map all technical components mentioned
semantic_search("technology stack frameworks libraries")
semantic_search("database tables schema models")
semantic_search("API endpoints routes controllers")
semantic_search("deployment infrastructure hosting")
```

#### 3. Repository Structure Discovery

```bash
# Find folder structures and organization
grep_search("repo|directory|folder|structure|tree", isRegexp=true)
grep_search("├──|└──|/\s*$", isRegexp=true)
```

#### 4. Document Creation Priority

1. **Repository_Structure.md** - Foundation for everything else
2. **README.md** - Project overview and navigation
3. **API_Documentation.md** - Technical contracts
4. **Database_Schema.md** - Data architecture
5. **Architecture_Overview.md** - System design
6. **Environment_Setup.md** - Configuration management
7. **Deployment_Guide.md** - Production deployment
8. **Development_Workflow.md** - Team processes

#### 5. Content Validation

```bash
# Check GitHub compliance for each created file
get_errors(["/path/to/created/file.md"])

# Validate all links and references work
# Ensure all code examples are functional
# Verify environment templates are complete
```

---

## 🎯 QUALITY CHECKPOINTS

### Before Declaring Surgery Complete

#### Content Quality Gates

- [ ] **All major technical decisions documented**
- [ ] **Repository structure is complete and logical**
- [ ] **API contracts are clearly defined**
- [ ] **Database schema is normalized and complete**
- [ ] **Environment configuration is security-compliant**
- [ ] **Deployment process is repeatable**

#### GitHub Compliance Gates

- [ ] **All markdown files pass lint validation**
- [ ] **Code blocks have language specifications**
- [ ] **Links are valid and accessible**
- [ ] **File structure follows conventions**
- [ ] **No placeholder or stub content**

#### Functional Verification Gates

- [ ] **README provides working quick start**
- [ ] **API documentation includes working examples**
- [ ] **Database schema can be executed**
- [ ] **Environment setup actually works**
- [ ] **Deployment guide produces working system**

---

## 🚨 COMMON EXTRACTION PITFALLS

### Content Pitfalls to Avoid

#### 1. Conversational Artifacts

- **Problem**: Including "Great!", "Perfect!", discussion fragments
- **Solution**: Extract only technical substance and decisions

#### 2. Incomplete Specifications

- **Problem**: Partial API definitions or database schemas
- **Solution**: Cross-reference and complete missing pieces

#### 3. Inconsistent Terminology

- **Problem**: Same concept called different names throughout
- **Solution**: Establish glossary and use consistently

#### 4. Missing Context

- **Problem**: Technical details without business rationale
- **Solution**: Include decision context and trade-offs

### Technical Pitfalls to Avoid

#### 1. GitHub Compliance Violations

- **Problem**: Markdown lint errors breaking validation
- **Solution**: Validate every file against GitHub standards

#### 2. Non-Functional Examples

- **Problem**: Code snippets that don't actually work
- **Solution**: Test all examples before including

#### 3. Security Anti-Patterns

- **Problem**: Hardcoded secrets in documentation
- **Solution**: Use .env.example templates only

#### 4. Broken Cross-References

- **Problem**: Links to non-existent files or sections
- **Solution**: Validate all internal links

---

## 📚 POST-SURGERY DOCUMENTATION

### Surgery Report Template

After completing extraction, create a surgery report:

```markdown
# Surgery Report: [PROJECT_NAME]

## Extraction Summary
- **Raw Material**: [filename]_Raw_Chat.yaml
- **Surgery Date**: [date]
- **Content Volume**: [lines of raw content]
- **Documents Created**: [count] files

## Documents Generated
- [ ] README.md
- [ ] Repository_Structure.md
- [ ] API_Documentation.md
- [ ] Database_Schema.md
- [ ] Architecture_Overview.md
- [ ] Environment_Setup.md
- [ ] Deployment_Guide.md

## Key Technical Decisions Extracted
- Technology Stack: [list]
- Architecture Patterns: [list]
- Database Design: [summary]
- Deployment Strategy: [summary]

## Compliance Status
- [ ] All markdown files pass GitHub validation
- [ ] All code examples are functional
- [ ] All environment variables are templated
- [ ] All links are valid

## Known Gaps
- [List any incomplete areas requiring future attention]

## Follow-Up Actions
- [List any remaining work or clarifications needed]
```

---

## 🔄 CONTINUOUS IMPROVEMENT

### Learning from Each Surgery

#### Track Extraction Patterns

- Common conversation structures in raw chats
- Frequently missed technical details
- Recurring compliance violations

#### Refine the Process

- Update extraction queries based on findings
- Improve document templates
- Enhance quality checkpoints

#### Build Knowledge Base

- Maintain library of working examples
- Document successful extraction patterns
- Create reusable template components

---

## 💡 PRO TIPS FOR SURGICAL SUCCESS

### 1. Start Broad, Then Narrow

- Use semantic_search for initial discovery
- Use grep_search for specific technical patterns
- Use read_file for detailed extraction

### 2. Validate as You Go

- Check GitHub compliance after each document
- Test code examples immediately
- Verify links and references continuously

### 3. Think Like the End User

- What would a new developer need to know?
- What would break if this was the only documentation?
- Can someone actually follow these instructions?

### 4. Maintain Traceability

- Link back to original raw chat content when needed
- Preserve decision rationale and context
- Document assumptions and constraints

---

**Remember: The goal is not just extraction, but transformation into production-ready, maintainable, GitHub-compliant project documentation that enables immediate development productivity.**
