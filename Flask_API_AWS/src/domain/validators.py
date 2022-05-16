from functools import wraps
from src.domain.exceptions import WrongFileExtensionModelException


def is_pdf(func: callable) -> callable:
    @wraps(func)
    def wrapper(code, dest_path):
        if dest_path.endswith(".pdf"):
            return func(code=code, dest_path=dest_path)
        raise WrongFileExtensionModelException("Wrong file extension: expected .pdf")
    return wrapper


def is_jpeg(func: callable) -> callable:
    @wraps(func)
    def wrapper(code, src_path):
        if src_path.endswith(".jpeg") or src_path.endswith(".jpg"):
            return func(code=code, src_path=src_path)
        raise WrongFileExtensionModelException("Wrong file extension: expected .jpeg or .jpg")
    return wrapper
