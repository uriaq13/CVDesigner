#!/usr/bin/env python3
"""Initialize and validate the candidate profile used by the CV skill."""

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA: dict[str, Any] = {
    "current_role": "",
    "target_roles": [],
    "summary": "",
    "contact": {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "links": [],
        "work_authorization": "",
    },
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "skills": {
        "technical": [],
        "domain": [],
        "interpersonal": [],
        "languages": [],
    },
    "additional": {
        "awards": [],
        "volunteering": [],
        "publications": [],
        "interview_formats": [],
        "preferences": {},
        "restrictions": [],
    },
}


def init_profile(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {output}")
    output.write_text(json.dumps(SCHEMA, indent=2) + "\n", encoding="utf-8")
    print(f"Created blank profile at {output}")


def validate_profile(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: profile does not exist: {path}")
        return 1
    except json.JSONDecodeError as error:
        print(f"ERROR: invalid JSON at {path}: {error}")
        return 1

    if not isinstance(data, dict):
        print("ERROR: profile root must be a JSON object")
        return 1

    missing = [key for key in SCHEMA if key not in data]
    if missing:
        print("ERROR: missing top-level fields: " + ", ".join(missing))
        return 1

    if not data.get("current_role") and not data.get("target_roles"):
        print("ERROR: provide current_role or at least one target_roles entry")
        return 1

    print(f"Profile is valid: {path}")
    print("Stored facts are user-supplied; empty fields remain unresolved.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="create a blank profile")
    init_parser.add_argument("--output", type=Path, required=True)

    validate_parser = commands.add_parser("validate", help="validate an existing profile")
    validate_parser.add_argument("--file", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "init":
        init_profile(args.output)
        return 0
    return validate_profile(args.file)


if __name__ == "__main__":
    raise SystemExit(main())
