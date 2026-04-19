class Message:
    def __init__(self, sender, receiver, content, metadata=None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.metadata = metadata or {}