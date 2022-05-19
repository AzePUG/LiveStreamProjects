class ConvertedListRequest:

    @classmethod
    def from_dict(cls, adict):
        return cls()

    def __bool__(self):
        return True


class ConvertedListInvalidRequest:

    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return True


class ConvertedListValidRequest:

    def __bool__(self):
        return True


def build_converted_list_request():
    invalid_req = ConvertedListInvalidRequest()

    # TODO: add the validation here, add if there is any error to invalid_req.add_error()

    if invalid_req.has_errors():
        return invalid_req

    return ConvertedListValidRequest()
