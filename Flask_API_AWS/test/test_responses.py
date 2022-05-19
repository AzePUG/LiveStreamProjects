from src.responses.responses import ResponseSuccess


def test_response_success_is_true():
    assert bool(ResponseSuccess)
