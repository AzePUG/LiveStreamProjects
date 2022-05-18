import dataclasses
import datetime
import uuid
from dataclasses import dataclass, field
from src.domain import validators


@dataclass
class JPG:
    code: uuid.UUID
    src_path: str
    extensions: tuple[str, str] = field(init=False, default=(".jpeg", ".jpg"))

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclass
class PDF:
    code: uuid.UUID
    dest_path: str
    extension: str = field(init=False, default=".pdf")

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclass
class Converted:
    converted_from: JPG
    converted_to: PDF
    converted_at: datetime.datetime

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return dataclasses.asdict(self)


@validators.is_jpeg
def allocate_jpeg(code: uuid.UUID, src_path: str) -> JPG:
    return JPG(code=code, src_path=src_path)


@validators.is_pdf
def allocate_pdf(code: uuid.UUID, dest_path: str) -> PDF:
    return PDF(code=code, dest_path=dest_path)
