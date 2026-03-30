#!/usr/bin/env python3
"""
Validates techpack.yaml structure for github-planner.

Usage:
    python src/utils/validate_techpack.py
    python src/utils/validate_techpack.py --file path/to/techpack.yaml

Exits with code 0 if valid, 1 if invalid.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

REQUIRED_TOP_LEVEL = ["schemaVersion", "identifier", "displayName", "description", "author"]
VALID_COMPONENT_TYPES = {"skill", "agent", "command", "hook", "settingsFile", "gitignore"}
VALID_PROMPT_TYPES = {"input", "select", "confirm"}


def error(msg):
    print(f"  ✗ {msg}")


def ok(msg):
    print(f"  ✓ {msg}")


def validate(path):
    print(f"Validating: {path}\n")
    failed = False

    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"✗ Invalid YAML: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ File not found: {path}")
        return False

    # Top-level required fields
    print("Required fields:")
    for field in REQUIRED_TOP_LEVEL:
        if field in data:
            ok(field)
        else:
            error(f"Missing required field: '{field}'")
            failed = True

    # schemaVersion must be an integer
    if "schemaVersion" in data:
        print("\nSchema version:")
        if isinstance(data["schemaVersion"], int):
            ok(f"schemaVersion is integer ({data['schemaVersion']})")
        else:
            error(f"schemaVersion must be an integer, got: {type(data['schemaVersion']).__name__}")
            failed = True

    # Validate prompts
    prompts = data.get("prompts", [])
    if prompts:
        print(f"\nPrompts ({len(prompts)}):")
        for i, prompt in enumerate(prompts):
            key = prompt.get("key", f"<prompt {i}>")
            if "key" not in prompt:
                error(f"Prompt {i} missing 'key'")
                failed = True
            if "type" not in prompt:
                error(f"Prompt '{key}' missing 'type'")
                failed = True
            elif prompt["type"] not in VALID_PROMPT_TYPES:
                error(f"Prompt '{key}' has invalid type '{prompt['type']}'")
                failed = True
            else:
                ok(f"{key} ({prompt['type']})")

    # Validate components
    components = data.get("components", [])
    if components:
        print(f"\nComponents ({len(components)}):")
        for comp in components:
            comp_id = comp.get("id", "<no id>")
            if "id" not in comp:
                error(f"Component missing 'id': {comp}")
                failed = True
                continue

            # Each component must have exactly one type
            comp_types = [t for t in VALID_COMPONENT_TYPES if t in comp]
            if not comp_types and "brew" not in comp and "doctorChecks" not in comp:
                error(f"'{comp_id}' has no recognizable component type")
                failed = True
            else:
                ok(comp_id)

            # Validate source paths exist
            for type_key in ["skill", "agent", "command", "hook"]:
                if type_key in comp:
                    source = comp[type_key].get("source")
                    if source:
                        source_path = Path(path).parent / source
                        if not source_path.exists():
                            error(f"'{comp_id}' source not found: {source}")
                            failed = True

    print()
    if failed:
        print("✗ Validation failed.")
        return False

    print("✓ techpack.yaml is valid.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate techpack.yaml structure")
    parser.add_argument(
        "--file",
        default="techpack.yaml",
        help="Path to techpack.yaml (default: techpack.yaml)",
    )
    args = parser.parse_args()

    success = validate(args.file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
