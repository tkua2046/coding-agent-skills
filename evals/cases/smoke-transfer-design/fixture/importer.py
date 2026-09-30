import json
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text())

def replace(path, text):
    Path(path).write_text(text)
    return load(path)
