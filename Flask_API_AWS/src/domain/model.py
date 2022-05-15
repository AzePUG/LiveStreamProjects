from dataclasses import dataclass, field


@dataclass
class JPG:
    src_path: str
    extensions: tuple[str, str] = field(init=False, default=(".jpeg", ".jpg"))


@dataclass
class PDF:
    dest_path: str
    extension: str = field(init=False, default=".pdf")
