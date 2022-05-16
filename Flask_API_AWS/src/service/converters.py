import img2pdf
import uuid
from PIL import Image
from src.domain import model
from src.service.validators import is_valid_jpg_path, is_valid_pdf_path
from contextlib import contextmanager
from typing import Generator


@is_valid_jpg_path
def jpg2pdf(jpg_path: str, pdf_path: str) -> None:
    jpg, pdf = _get_jpg_pdf(jpg_path, pdf_path)
    with _open_jpg(jpg.src_path) as image:
        _convert_and_save_pdf(image, pdf)


def _convert_and_save_pdf(image, pdf) -> None:
    pdf_bytes = _convert_to_pdf(image)
    with _create_pdf(pdf.dest_path) as file:
        file.write(pdf_bytes)


def _convert_to_pdf(image) -> bytes:
    return img2pdf.convert(image.filename)


def _get_jpg_pdf(jpg_path, pdf_path) -> tuple[model.JPG, model.PDF]:
    jpg = model.allocate_jpeg(code=uuid.uuid4(), src_path=jpg_path)
    pdf = model.allocate_pdf(code=uuid.uuid4(), dest_path=pdf_path)
    return jpg, pdf


@contextmanager
def _open_jpg(img_path: str) -> Generator:
    try:
        image = Image.open(img_path)
        yield image
    finally:
        image.close()


@is_valid_pdf_path
@contextmanager
def _create_pdf(pdf_path: str) -> Generator:
    try:
        file = open(pdf_path, "wb")
        yield file
    finally:
        file.close()
