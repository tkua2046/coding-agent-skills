import json


def load(path):
    with open(path, encoding="utf-8") as stream:
        data = json.load(stream)
    if data.get("version") != 1:
        raise ValueError("unsupported settings version")
    entries = data["entries"]
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate entry id")
    return {entry["id"]: entry["value"] for entry in entries}
