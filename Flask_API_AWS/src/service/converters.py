import img2pdf
from PIL import Image
from src.domain import model
from src.service.validators import is_valid_jpg_path, is_valid_pdf_path
from contextlib import contextmanager


@is_valid_jpg_path
def jpg2pdf(jpg_path: str, pdf_path: str) -> None:
    jpg, pdf = _get_jpg_pdf(jpg_path, pdf_path)
    with _open_jpg(jpg.src_path) as image:
        _convert_and_save_pdf(image, pdf)


def _convert_and_save_pdf(image, pdf):
    pdf_bytes = img2pdf.convert(image.filename)
    with _create_pdf(pdf.dest_path) as file:
        file.write(pdf_bytes)


def _get_jpg_pdf(jpg_path, pdf_path):
    jpg = model.allocate_jpeg(src_path=jpg_path)
    pdf = model.allocate_pdf(dest_path=pdf_path)
    return jpg, pdf


@contextmanager
def _open_jpg(img_path: str):
    try:
        image = Image.open(img_path)
        yield image
    finally:
        image.close()


@is_valid_pdf_path
@contextmanager
def _create_pdf(pdf_path: str):
    try:
        file = open(pdf_path, "wb")
        yield file
    finally:
        file.close()
