from src.responses.responses import ResponseSuccess, ResponseFailure, ResponseTypes, build_response_from_invalid_request
from src.requests.converted_list import ConvertedListInvalidRequest

SUCCESS_VALUE = {"key": ["value1", "value2"]}
GENERIC_RESPONSE_TYPE = "Response"
GENERIC_RESPONSE_MESSAGE = "This is a response"


def test_response_success_is_true():
    response = ResponseSuccess(SUCCESS_VALUE)
    assert bool(response)


def test_response_failure_is_false():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE
    )
    assert not bool(response)


def test_response_success_has_type_and_value():
    response = ResponseSuccess(SUCCESS_VALUE)

    assert response.type == ResponseTypes.SUCCESS
    assert response.value == SUCCESS_VALUE


def test_response_failure_has_type_and_massage():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE
    )

    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == GENERIC_RESPONSE_MESSAGE
    assert response.value == {
        "type": GENERIC_RESPONSE_TYPE,
        "message": GENERIC_RESPONSE_MESSAGE
    }


def test_response_failure_initialization_with_exception():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, Exception("Just an error message")
    )
    assert not bool(response)
    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == "Exception: Just an error message"


def test_response_failure_from_empty_invalid_request():
    response = build_response_from_invalid_request(
        ConvertedListInvalidRequest()
    )

    assert not bool(response)
    assert response.type == ResponseTypes.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_with_errors():
    request = ConvertedListInvalidRequest()
    request.add_error("path", "JPEG path is mandatory")

    response = build_response_from_invalid_request(request)
    assert not bool(response)
    assert response.type == ResponseTypes.PARAMETERS_ERROR
    assert response.message == "path: JPEG path is mandatory"


