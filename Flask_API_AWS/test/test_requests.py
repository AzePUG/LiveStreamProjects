from src.requests.converted_list import ConvertedListRequest


def test_build_converted_list_request_without_parameters():
    request = ConvertedListRequest()
    assert bool(request)


def test_build_converted_list_request_from_emtpy_dict():
    request = ConvertedListRequest.from_dict({})
    assert bool(request)