class Message:
    def __init__(self, sender_id, receiver_id, message_type, content=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type
        self.content = content
