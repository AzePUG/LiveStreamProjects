import json
import uuid
import datetime

from flask import Blueprint, Response

from src.repository.memrepo import MemRepo
from src.requests.converted_list import build_converted_list_request
from src.serializers.model import ConvertedJsonEncoder
from src.use_cases.converted_list import converted_list_use_case
from src.domain import model
from src.responses.responses import ResponseTypes

blueprint = Blueprint("convert", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


def _get_converted_list():
    jpg = model.JPG(code=uuid.uuid4(), src_path="fake.jpg")
    pdf = model.PDF(code=uuid.uuid4(), dest_path="fake.pdf")
    return [
        {
            "converted_from": jpg,
            "converted_to": pdf,
            "converted_at": datetime.datetime.now()
        },
        {
            "converted_from": jpg,
            "converted_to": pdf,
            "converted_at": datetime.datetime.now()
        },
        {
            "converted_from": jpg,
            "converted_to": pdf,
            "converted_at": datetime.datetime.now()
        },
        {
            "converted_from": jpg,
            "converted_to": pdf,
            "converted_at": datetime.datetime.now()
        }
    ]


@blueprint.route("/converteds", methods=["GET"])
def room_list():
    request_object = build_converted_list_request()
    repo = MemRepo(_get_converted_list())
    response = converted_list_use_case(repo, request_object)
    return Response(
        json.dumps(response.value, cls=ConvertedJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type]
    )

