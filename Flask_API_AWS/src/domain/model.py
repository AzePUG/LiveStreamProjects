from dataclasses import dataclass, field
from src.domain import validators


@dataclass
class JPG:
    src_path: str
    extensions: tuple[str, str] = field(init=False, default=(".jpeg", ".jpg"))


@dataclass
class PDF:
    dest_path: str
    extension: str = field(init=False, default=".pdf")


@validators.is_jpeg
def allocate_jpeg(src_path: str) -> JPG:
    return JPG(src_path=src_path)


@validators.is_pdf
def allocate_pdf(dest_path: str) -> PDF:
    return PDF(dest_path=dest_path)
