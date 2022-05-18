import uuid

import pytest

from src.entrypoints.api.app import create_app
from src.domain import model


@pytest.fixture
def get_uuid():
    return uuid.uuid4()


@pytest.fixture
def app():
    return create_app("testing")


@pytest.fixture
def converted_data(get_uuid):
    jpg = model.JPG(code=get_uuid, src_path="fake.jpg")
    pdf = model.PDF(code=get_uuid, dest_path="fake.pdf")
    converted_1 = model.Converted(converted_from=jpg, converted_to=pdf)
    converted_2 = model.Converted(converted_from=jpg, converted_to=pdf)
    converted_3 = model.Converted(converted_from=jpg, converted_to=pdf)
    converted_4 = model.Converted(converted_from=jpg, converted_to=pdf)
    return [converted_1, converted_2, converted_3, converted_4]
