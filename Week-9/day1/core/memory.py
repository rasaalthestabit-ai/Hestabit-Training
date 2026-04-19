class Memory:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.messages = []

    def add(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_size:
            self.messages.pop(0)

    def get_context(self):
        return "\n".join([m.content for m in self.messages])