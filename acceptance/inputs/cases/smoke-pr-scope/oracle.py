"""Keep PR preparation from rewriting the completed feature or its required example."""

import hashlib
from pathlib import Path

EXPECTED = {'task_report.py': 'a64f2160b0b11cb8c7fa8bb73c8d679569d5cd1f72a2d2c4d5ecafd5f5c4067c', 'tests/test_task_report.py': '6e881b6f8d9ff68c9d9da7ad01b2cf05eea6dccc8daa0fba01729bf66b1f7e92', 'examples/open-tasks.csv': 'ab4690ef4a9498f093d3857aadbd401ff06e39b34d2d36aa703414a5bed53cea'}

for name, expected in EXPECTED.items():
    path = Path(name)
    assert path.is_file(), f"Missing required feature file: {name}"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Feature changed during PR preparation: {name}"
