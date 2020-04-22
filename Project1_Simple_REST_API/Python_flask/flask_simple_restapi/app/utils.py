from extensions.extension import pwd_context
from flask import current_app
import re




def verify_secret(plain_secret: str, hashed_secret: str):
    """ check plain password with hashed password """

    return pwd_context.verify(plain_secret, hashed_secret)


def get_secret_hash(secret: str):
    """ return hash plain text """
    
    return pwd_context.hash(secret)