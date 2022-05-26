from unittest import mock

from src.requests.converted_list import ConvertedListRequest, build_converted_list_request
from src.use_cases.converted_list import converted_list_use_case


def test_converted_list_without_parameters(converted_data):
    repo = mock.Mock()
    repo.list.return_value = converted_data
    request = build_converted_list_request()
    response = converted_list_use_case(repo, request)
    assert bool(response)
    repo.list.assert_called_with()
    assert response.value == converted_data
