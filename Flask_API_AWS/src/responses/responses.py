class ResponseSuccess:

    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return True
