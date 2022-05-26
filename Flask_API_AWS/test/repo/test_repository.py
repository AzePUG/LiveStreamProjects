from src.domain.model import Converted
from src.repository.memrepo import MemRepo


def test_repository_list_without_parameters(converted_dicts):
    repo = MemRepo(converted_dicts)
    converted_list = [Converted.from_dict(i) for i in converted_dicts]
    assert repo.list() == converted_list
