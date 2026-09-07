class Session:
    def __init__(self):
        self.cursor = 4
        self.selection = "open"
    def apply(self, command):
        self.selection = "closed"
        if command not in {"next", "previous"}:
            raise ValueError("unknown command")
        self.selection = "closed"
        self.cursor += 1 if command == "next" else -1
