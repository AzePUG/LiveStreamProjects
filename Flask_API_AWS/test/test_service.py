import os

import pytest

from src.domain.exceptions import WrongFileExtensionModelException
from src.service import converters


def test_if_jpg_converted_to_pdf():
    jpg_path = os.path.abspath("test/data/AzePUG.jpg")
    pdf_path = os.path.abspath("test/data/AzePUG.pdf")
    converters.jpg2pdf(jpg_path, pdf_path)
    assert os.path.isfile(pdf_path)


def test_with_wrong_jpg_path():
    jpg_path = os.path.abspath("./data/AzePUG.jpg")
    pdf_path = os.path.abspath("test/data/AzePUG.pdf")
    with pytest.raises(FileNotFoundError) as err:
        converters.jpg2pdf(jpg_path, pdf_path)
    assert str(err.value) == "Wrong jpg file path provided"


def test_with_wrong_pdf_path():
    jpg_path = os.path.abspath("test/data/AzePUG.jpg")
    pdf_path = os.path.abspath("test/asdsad/AzePUG.pdf")
    with pytest.raises(FileNotFoundError) as err:
        converters.jpg2pdf(jpg_path, pdf_path)
    assert str(err.value) == "Wrong pdf file path provided"


def test_with_wrong_format():
    jpg_path = os.path.abspath("test/data/wrong_format.txt")
    pdf_path = os.path.abspath("test/asdsad/AzePUG.pdf")
    with pytest.raises(WrongFileExtensionModelException) as err:
        converters.jpg2pdf(jpg_path, pdf_path)
    assert str(err.value) == "Wrong file extension: expected .jpeg or .jpg"
