import uuid
from dataclasses import dataclass, field
from src.domain import validators


@dataclass
class JPG:
    code: uuid.UUID
    src_path: str
    extensions: tuple[str, str] = field(init=False, default=(".jpeg", ".jpg"))


@dataclass
class PDF:
    code: uuid.UUID
    dest_path: str
    extension: str = field(init=False, default=".pdf")


@validators.is_jpeg
def allocate_jpeg(code: uuid.UUID, src_path: str) -> JPG:
    return JPG(code=code, src_path=src_path)


@validators.is_pdf
def allocate_pdf(code: uuid.UUID, dest_path: str) -> PDF:
    return PDF(code=code, dest_path=dest_path)
