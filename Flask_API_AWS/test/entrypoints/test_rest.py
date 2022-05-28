import datetime
import json
import uuid
import pytest
from unittest import mock

from src.domain import model
from src.domain.model import Converted
from src.serializers.model import ConvertedJsonEncoder
from src.responses.responses import ResponseFailure, ResponseSuccess, ResponseTypes


def _get_converted(timestamp_: datetime.datetime, uuid_: uuid.UUID):
    jpg = model.JPG(code=uuid_, src_path="fake.jpg")
    pdf = model.PDF(code=uuid_, dest_path="fake.pdf")
    return {
        "converted_from": jpg,
        "converted_to": pdf,
        "converted_at": timestamp_
    }


def _converted_list(get_uuid: uuid.UUID) -> list[Converted]:
    timestamp_ = datetime.datetime.now()
    return [Converted.from_dict(_get_converted(timestamp_, get_uuid))]


@mock.patch("src.entrypoints.api.rest.convert.converted_list_use_case")
def test_get(mock_user_case, client, get_uuid):
    converted_list = _converted_list(get_uuid)
    mock_user_case.return_value = ResponseSuccess(converted_list)
    http_response = client.get("/converteds")
    assert json.loads(http_response.data.decode("UTF-8")) == json.loads(
        json.dumps(converted_list, cls=ConvertedJsonEncoder))
    mock_user_case.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@pytest.mark.parametrize(
    "response_type, expected_status_code",
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ]
)
@mock.patch("src.entrypoints.api.rest.convert.converted_list_use_case")
def test_get_response_failures(mock_use_case, client, response_type, expected_status_code):
    mock_use_case.return_value = ResponseFailure(response_type, message="Just an error message")
    http_response = client.get("/converteds")
    mock_use_case.assert_called()
    assert http_response.status_code == expected_status_code
