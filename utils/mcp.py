import uuid
import datetime

class MCPMessage:
    def __init__(self, sender, receiver, type, payload, trace_id=None):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.trace_id = trace_id or str(uuid.uuid4())
        self.timestamp = datetime.datetime.now().isoformat()
        self.payload = payload

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }