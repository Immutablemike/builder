#!/usr/bin/env python3
import json
import pathlib

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "briefs"


def validate_manifest(path):
    print(f"🧩 Validating {path.name}")
    with open(path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    schema = {"type": "object", "required": ["project", "components"]}
    jsonschema.validate(spec, schema)
    return spec


def generate_docs(spec, name):
    out_api = ROOT / f"{name}_API_OpenAPI.yaml"
    out_schema = ROOT / f"{name}_API_Schema.json"
    schemas = spec["components"]["schemas"]
    openapi = {
        "openapi": "3.1.0",
        "info": {"title": spec["project"], "version": spec["version"]},
        "paths": {},
        "components": {"schemas": schemas},
    }
    with open(out_api, "w", encoding="utf-8") as f:
        yaml.safe_dump(openapi, f)
    with open(out_schema, "w", encoding="utf-8") as f:
        json.dump(schemas, f, indent=2)
    print(f"✅ Docs written → {out_api}, {out_schema}")


def create_output_dir(name):
    out = ROOT / f"{name}_complete"
    out.mkdir(exist_ok=True)
    readme_content = f"# {name}\nAuto-generated project.\n"
    (out / "README.md").write_text(readme_content, encoding="utf-8")
    return out


def main():
    import sys
    if len(sys.argv) > 1:
        # Process specific file from command line
        brief_path = pathlib.Path(sys.argv[1])
        if brief_path.exists():
            name = brief_path.stem.replace("_Stack", "")
            spec = validate_manifest(brief_path)
            generate_docs(spec, name)
            out = create_output_dir(name)
            print(f"✅ Processed {brief_path.name}")
        else:
            print(f"❌ File not found: {brief_path}")
    else:
        # Process all files in briefs directory
        for brief in BRIEFS.glob("*_Stack.yaml"):
            name = brief.stem.replace("_Stack", "")
            spec = validate_manifest(brief)
            generate_docs(spec, name)
            out = create_output_dir(name)
            print(f"🧠 Project folder ready: {out}")


if __name__ == "__main__":
    main()
