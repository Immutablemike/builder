#!/usr/bin/env python3
"""
Pure Copilot CLI Factory Controller
Manages the complete workflow chain for Copilot CLI generation
"""
import subprocess
import sys
from pathlib import Path

import yaml


def trigger_copilot_generation(brief_path: str) -> None:
    """Trigger the Copilot CLI generation workflow."""
    try:
        # Validate brief exists and is readable
        brief = Path(brief_path)
        if not brief.exists():
            print(f"❌ Brief file not found: {brief_path}")
            sys.exit(1)
        
        # Load brief to get project name
        with open(brief, encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        
        project_name = spec.get("project", brief.stem.replace("_Stack", ""))
        print(f"🚀 Triggering Copilot CLI generation for: {project_name}")
        
        # Trigger GitHub Actions workflow
        cmd = [
            "gh", "workflow", "run", "03_production_generate.yml",
            "-f", f"brief_file={brief_path}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Copilot CLI workflow triggered for {project_name}")
            print("🎯 Check GitHub Actions for generation progress")
        else:
            print(f"❌ Failed to trigger workflow: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for Copilot CLI factory control."""
    if len(sys.argv) != 2:
        print("Usage: python copilot_factory.py <brief_file.yaml>")
        print("Example: python copilot_factory.py briefs/ToySoldiers_Stack.yaml")
        sys.exit(1)
    
    trigger_copilot_generation(sys.argv[1])


if __name__ == "__main__":
    main()