import datetime
import json
import uuid
from unittest import mock

from src.domain import model
from src.domain.model import Converted
from src.serializers.model import ConvertedJsonEncoder


def _get_converted(timestamp_: datetime.datetime, uuid_: uuid.UUID):
    jpg = model.JPG(code=uuid_, src_path="fake.jpg")
    pdf = model.PDF(code=uuid_, dest_path="fake.pdf")
    return {
        "converted_from": jpg,
        "converted_to": pdf,
        "converted_at": timestamp_
    }


@mock.patch("src.entrypoints.api.rest.convert.converted_list_use_case")
def test_get(mock_user_case, client, get_uuid):
    timestamp_ = datetime.datetime.now()
    converted_list = [Converted.from_dict(_get_converted(timestamp_, get_uuid))]
    mock_user_case.return_value = converted_list
    http_response = client.get("/converteds")
    assert json.loads(http_response.data.decode("UTF-8")) == json.loads(
        json.dumps(converted_list, cls=ConvertedJsonEncoder))
    mock_user_case.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"
