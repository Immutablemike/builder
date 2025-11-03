# Builder System - Project Generation Makefile
# =============================================

.PHONY: help generate-project validate-briefs list-briefs clean-generated

# Default target
help: ## 📋 Show this help message
	@echo "🏗️  Builder System - Project Generation Commands"
	@echo "=============================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Project Generation
generate-project: ## 🚀 Generate project from brief (usage: make generate-project BRIEF=briefs/MyProject_Stack.yaml)
	@if [ -z "$(BRIEF)" ]; then \
		echo "❌ Error: BRIEF parameter required"; \
		echo "📋 Usage: make generate-project BRIEF=briefs/MyProject_Stack.yaml"; \
		exit 1; \
	fi
	@echo "🚀 Generating project from $(BRIEF)..."
	@python3 tools/project_generator.py "$(BRIEF)"
	@echo "✅ Project generation complete!"

validate-briefs: ## ✅ Validate all brief files
	@echo "✅ Validating brief files..."
	@for file in briefs/*_Stack.yaml; do \
		if [ -f "$$file" ]; then \
			echo "🔍 Validating $$file"; \
			python3 -c "import yaml; yaml.safe_load(open('$$file'))" || exit 1; \
		fi; \
	done
	@echo "✅ All brief files validated!"

list-briefs: ## 📋 List available brief files
	@echo "📋 Available Brief Files:"
	@echo "========================"
	@for file in briefs/*_Stack.yaml; do \
		if [ -f "$$file" ]; then \
			echo "  📄 $$file"; \
		fi; \
	done

clean-generated: ## 🧹 Clean generated project directories
	@echo "🧹 Cleaning generated projects..."
	@rm -rf *_complete/
	@echo "✅ Generated projects cleaned!"

# Setup and Installation
setup: ## 📦 Install dependencies for project generation
	@echo "📦 Installing project generation dependencies..."
	@pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Quick project generation workflow
quick-generate: validate-briefs ## 🚀 Quick project generation (validates then generates)
	@echo "🚀 Quick Project Generation Workflow"
	@echo "===================================="
	@$(MAKE) list-briefs
	@echo ""
	@echo "📋 Usage: make generate-project BRIEF=briefs/YourProject_Stack.yaml"