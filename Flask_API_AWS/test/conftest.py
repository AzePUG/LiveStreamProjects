import uuid

import pytest

from src.entrypoints.api.app import create_app


@pytest.fixture
def get_uuid():
    return uuid.uuid4()


@pytest.fixture
def app():
    return create_app("testing")
