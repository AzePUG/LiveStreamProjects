import pytest

from src.entrypoints.api.app import create_app


@pytest.fixture
def app():
    return create_app("testing")
