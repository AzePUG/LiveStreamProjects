def is_pdf(src: str) -> bool:
    return src.endswith(".pdf")


def is_jpeg(src: str) -> bool:
    return src.endswith(".jpeg") or src.endswith(".jpg")
