import os
from src.service import converters


def test_if_jpg_converted_to_pdf():
    jpg_path = os.path.abspath("test/data/AzePUG.jpg")
    pdf_path = os.path.abspath("test/data/AzePUG.pdf")
    converters.jpg2pdf(jpg_path, pdf_path)
    assert os.path.isfile(pdf_path)
