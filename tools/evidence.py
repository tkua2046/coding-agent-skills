"""Persist each trial independently without replacing earlier evidence."""

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def write_report(directory: Path, payload: dict) -> Path:
    content = json.dumps(payload, indent=2) + "\n"
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    path = directory / f"{stamp}-{uuid4().hex}.json"
    with path.open("x") as stream:
        stream.write(content)
    return path
