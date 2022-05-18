from unittest import mock

from src.use_cases.converted_list import converted_list_use_case


def test_converted_list_without_parameters(converted_data):
    repo = mock.Mock()
    repo.list.return_value = converted_data
    result = converted_list_use_case(repo)
    repo.list.assert_called_with()
    assert result == converted_data
