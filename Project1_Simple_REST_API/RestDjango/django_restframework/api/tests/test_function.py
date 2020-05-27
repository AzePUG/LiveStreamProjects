from django.test import  SimpleTestCase
from api.utils import  jwt_decode_handler
from django.conf import settings
from jwt.exceptions import  ExpiredSignatureError



class TestFunc(SimpleTestCase):


    def test_jwt(self):

        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkwNTczMzIzLCJqdGkiOiI2YjVkZDBhOGU0ZDE0YzMzODQwM2ZiZWFiZjE3ZmE0MSIsInVzZXJfaWQiOjEwfQ.WZFnpB805o045MJnzqhsMit6p30mu-2TVgA6oitYWI0"
        result = {'token_type': 'access', 'exp': 1590573323, 'jti': '6b5dd0a8e4d14c338403fbeabf17fa41', 'user_id': 10}

        with self.assertRaises(ExpiredSignatureError) as expired:


            self.assertEqual(jwt_decode_handler(token),result)
        self.assertEqual(ExpiredSignatureError, type(expired.exception))  

    