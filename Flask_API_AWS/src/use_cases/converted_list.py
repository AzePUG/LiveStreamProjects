from src.responses.responses import ResponseSuccess, build_response_from_invalid_request, ResponseFailure, ResponseTypes


def converted_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        converteds = repo.list()
        return ResponseSuccess(converteds)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
