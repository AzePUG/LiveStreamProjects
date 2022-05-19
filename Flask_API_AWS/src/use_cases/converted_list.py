from src.responses.responses import ResponseSuccess


def converted_list_use_case(repo, request):
    converteds = repo.list()
    return ResponseSuccess(converteds)
