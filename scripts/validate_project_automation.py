from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / ".github" / "project-board.json"
MAPPING_PATH = ROOT / ".github" / "project-label-mapping.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "project-automation.yml"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    for path in (BOARD_PATH, MAPPING_PATH, WORKFLOW_PATH):
        if not path.exists():
            fail(f"Missing required file: {path.relative_to(ROOT)}")

    board = json.loads(BOARD_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    board_fields = {
        field["name"]: set(field.get("options", []))
        for field in board.get("fields", [])
    }

    for field_name, labels in mapping.items():
        if field_name not in board_fields:
            fail(f"Mapped field is missing from project-board.json: {field_name}")
        for label, option in labels.items():
            if not label.strip():
                fail(f"Blank label configured for field {field_name}")
            if option not in board_fields[field_name]:
                fail(
                    f"Mapped option '{option}' is not configured for field '{field_name}'"
                )

    required_fragments = (
        "workflow_dispatch:",
        "PROJECT_TOKEN",
        "project-label-mapping.json",
        "updateProjectV2ItemFieldValue",
    )
    for fragment in required_fragments:
        if fragment not in workflow:
            fail(f"Workflow is missing required fragment: {fragment}")

    print("Project automation configuration is valid.")


if __name__ == "__main__":
    main()
