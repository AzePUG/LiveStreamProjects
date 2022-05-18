from src.domain.model import Converted


class MemRepo:

    def __init__(self, data):
        self.data = data

    def list(self):
        return [Converted.from_dict(i) for i in self.data]