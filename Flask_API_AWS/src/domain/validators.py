from functools import wraps
from src.domain.exceptions import WrongFileExtensionModelException


def is_pdf(func: callable) -> callable:
    @wraps(func)
    def wrapper(dest_path):
        if dest_path.endswith(".pdf"):
            return func(dest_path=dest_path)
        raise WrongFileExtensionModelException("Wrong file extension: expected .pdf")
    return wrapper


def is_jpeg(func: callable) -> callable:
    @wraps(func)
    def wrapper(src_path):
        if src_path.endswith(".jpeg") or src_path.endswith(".jpg"):
            return func(src_path=src_path)
        raise WrongFileExtensionModelException("Wrong file extension: expected .jpeg or .jpg")
    return wrapper
