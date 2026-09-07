def normalize_names(names):
    result = set()
    for name in names:
        if not name or ".." in name.split("/"):
            raise ValueError("invalid package entry")
        result.add(name)
    return sorted(result)
