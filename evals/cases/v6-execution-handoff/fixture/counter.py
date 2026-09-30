class Counter:
    def __init__(self, value=0):
        self.value = value

    def add(self, step=1):
        self.value += step
        return self.value
