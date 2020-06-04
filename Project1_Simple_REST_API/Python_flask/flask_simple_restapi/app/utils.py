from extensions.extension import pwd_context
from flask import current_app
from app.custom_errors import PasswordLength




def verify_secret(plain_secret: str, hashed_secret: str):
    """ check plain password with hashed password """
    if len(plain_secret) < 8:
        raise PasswordLength("password length must be more than 8 or equal to 8")
    return pwd_context.verify(plain_secret, hashed_secret)


def get_secret_hash(secret: str):
    """ return hash plain text """
    if len(secret) < 8:
        raise PasswordLength("password length must be more than 8 or equal to 8")
    return pwd_context.hash(secret)