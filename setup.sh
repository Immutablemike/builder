#!/bin/bash
# Setup script for the YAML-to-Codebase Factory

echo "🚀 Setting up YAML-to-Codebase Factory..."

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found. Copy .env.example to .env and configure your tokens."
    echo "   Required: GH_TOKEN with Copilot Requests permission"
fi

# Check Node.js version (required for new Copilot CLI)
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "   Install Node.js v22+ for GitHub Copilot CLI support"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "❌ Node.js v22+ is required for GitHub Copilot CLI (current: v$NODE_VERSION)"
    echo "   Please upgrade Node.js to v22 or higher"
    exit 1
fi

# Install GitHub Copilot CLI (new version)
echo "🤖 Installing GitHub Copilot CLI..."
npm install -g @github/copilot

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x tools/export_repo.sh

# Create Copilot CLI trusted directories configuration
echo "🔧 Configuring Copilot CLI trusted directories..."
mkdir -p ~/.copilot
if [ ! -f ~/.copilot/config.json ]; then
    echo '{"trusted_folders": ["/github/workspace", "'$(pwd)'"]}' > ~/.copilot/config.json
    echo "   Added $(pwd) to trusted directories"
fi

# Generate initial documentation
echo "📚 Generating initial documentation..."
python3 tools/build_docs.py

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is installed"
else
    echo "⚠️  GitHub CLI not found. Please install it:"
    echo "   macOS: brew install gh"
    echo "   Ubuntu: sudo apt install gh"
    echo "   Or visit: https://cli.github.com/"
fi

# Check new Copilot CLI installation
if command -v copilot &> /dev/null; then
    echo "✅ New GitHub Copilot CLI is installed"
    copilot --version
else
    echo "❌ GitHub Copilot CLI installation failed"
fi

echo ""
echo "🎯 Setup complete! Next steps:"
echo "1. Verify .env contains your GitHub token with Copilot permissions"
echo "2. Add your YAML manifests to briefs/"
echo "3. Push to trigger the pipeline"
echo "4. Comment ✅ on confirmation issues to approve builds"
echo ""
echo "Local usage:"
echo "  python3 tools/build_docs.py    # Generate docs locally"
echo "  ./tools/export_repo.sh [dir] [repo]  # Export to new repo"
echo "  copilot  # Start interactive Copilot CLI"
echo ""
echo "🔑 Authentication Status:"
echo "  - GH_TOKEN: $(if [ -n "$GH_TOKEN" ]; then echo "✅ Configured"; else echo "❌ Missing"; fi)"
echo "  - Node.js: $(node -v)"
echo "  - Copilot CLI: $(if command -v copilot &> /dev/null; then echo "✅ Ready"; else echo "❌ Missing"; fi)"