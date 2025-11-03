#!/usr/bin/env python3
"""
Project Generator for Builder System
Generates complete project structures from YAML manifests
GitHub Compliance: Python 3.11+, type hints, proper error handling
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import yaml
from jinja2 import Environment, FileSystemLoader


class ProjectGenerator:
    """Generate complete project structures from YAML manifests."""
    
    def __init__(self, brief_path: str) -> None:
        """Initialize project generator with brief file path."""
        self.brief_path = Path(brief_path)
        self.brief_name = self.brief_path.stem.replace("_Stack", "")
        self.output_dir = Path(f"{self.brief_name}_complete")
        self.template_dir = Path("templates/toysoldiers")
        
    def load_manifest(self) -> Dict[str, Any]:
        """Load and parse the project manifest YAML."""
        try:
            with open(self.brief_path, encoding="utf-8") as f:
                manifest = yaml.safe_load(f)
                
            # Validate required fields for ToySoldiers template
            required_fields = ["project_meta", "repo_tree", "environments"]
            for field in required_fields:
                if field not in manifest:
                    print(f"❌ Error: Missing required field '{field}'")
                    sys.exit(1)
                    
            return manifest
        except FileNotFoundError:
            print(f"❌ Error: Brief file not found: {self.brief_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML: {e}")
            sys.exit(1)
    
    def extract_template_vars(
        self, manifest: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract template variables from manifest."""
        components = manifest.get("components", {})
        api = components.get("api", {})
        
        return {
            "project_name": manifest.get("project", self.brief_name),
            "description": manifest.get("description", ""),
            "version": manifest.get("version", "1.0.0"),
            "api_base_url": api.get("base_url", ""),
            "infrastructure": manifest.get("infrastructure", {}),
            "environments": manifest.get("environments", {}),
            "components": components,
        }
    
    def render_templates(self, template_vars: Dict[str, Any]) -> None:
        """Render all template files with project variables."""
        env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Process all template files
        for template_file in self.template_dir.rglob("*.j2"):
            rel_path = template_file.relative_to(self.template_dir)
            output_path = self.output_dir / str(rel_path).replace(".j2", "")
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Render template
            template = env.get_template(str(rel_path))
            rendered = template.render(**template_vars)
            
            # Write rendered file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)
    
    def generate_project(self) -> None:
        """Main generation workflow."""
        print(f"🚀 Generating project: {self.brief_name}")
        
        # Load manifest
        manifest = self.load_manifest()
        template_vars = self.extract_template_vars(manifest)
        
        # Render templates
        self.render_templates(template_vars)
        
        # Initialize git repository
        try:
            subprocess.run(
                ["git", "init"], cwd=self.output_dir, check=True
            )
            subprocess.run(
                ["git", "add", "."], cwd=self.output_dir, check=True
            )
            commit_msg = f"Initial commit for {self.brief_name}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.output_dir,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            sys.exit(1)
        
        print(f"✅ Project generated in {self.output_dir}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python project_generator.py <brief_file.yaml>")
        sys.exit(1)
    
    generator = ProjectGenerator(sys.argv[1])
    generator.generate_project()


if __name__ == "__main__":
    main()