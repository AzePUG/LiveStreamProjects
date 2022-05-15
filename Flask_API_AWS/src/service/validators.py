from functools import wraps
import os


def is_valid_jpg_path(func):
    @wraps(func)
    def wrapper(jpg_path: str, _: str):
        if not os.path.isfile(jpg_path):
            raise FileNotFoundError("Wrong jpg file path provided")
        return func(jpg_path, _)

    return wrapper


def is_valid_pdf_path(func):
    @wraps(func)
    def wrapper(pdf_path):
        if not os.path.exists(os.path.dirname(pdf_path)):
            raise FileNotFoundError("Wrong pdf file path provided")
        return func(pdf_path)
    return wrapper
