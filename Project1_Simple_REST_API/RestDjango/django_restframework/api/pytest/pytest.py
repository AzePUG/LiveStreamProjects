import pytest


# You can test your Django application without using a Library but pytest offers some features that are not present in Django’s standard test mechanism: :

# Detailed info on failing assert statements (no need to remember self.assert* names);
# Auto-discovery of test modules and functions;
# Modular fixtures for managing small or parametrized long-lived test resources;
# Can run unit test (including trial) and nose test suites out of the box;
#to run test with multiple markeers use dec  

#wherner we need to run some code before test we use pytets fixture

# def func(x):
#     return x + 5


# def test_method():
#     assert func(3) ==8


# pytest.fxiture replament deye bilerik setupdaki eslinde


@pytest.fixture
def numbers():
    a = 10
    b = 15
    c = 10
    return [a,b,c]

#so below two methods is going to be used for oyfuxture

# @pytest.mark.skip #this will skip the test
def method_test(numbers):
    x = 13
    assert numbers[1] == 15