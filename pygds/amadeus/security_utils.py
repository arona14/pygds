import uuid
from time import gmtime, strftime
import secrets
import base64
from hashlib import sha1


def generate_random_message_id(prefix: str = ""):
    """
        This function generate a random message id with a given prefix
    """
    return prefix + str(uuid.uuid4())


def generate_nonce(n_bytes=16):
    """
        This function generates a nonce value and base64 encode it
    """
    nonce = base64.encodebytes(secrets.token_bytes(n_bytes))
    return str(nonce)[2:-3]


def generate_created():
    """
        Generates the created date of a nonce based on the current datetime and format it
    """
    return str(strftime("%Y-%m-%dT%H:%M:%S.%zZ", gmtime()))


def password_digest(password: str, nonce: str, created: str):
    """
        Digest a password as needed by Amadeus. The digest is based on password, nonce and created datetie
    """
    if None in (password, nonce, created):
        raise ValueError("password, nonce or created cannot be null")
    sha_pwd = sha1()
    sha_pwd.update(password.encode('utf-8'))
    result = sha1()
    result.update(base64.b64decode(nonce))
    result.update(created.encode('utf-8'))
    result.update(sha_pwd.digest())
    hashed = base64.b64encode(result.digest())
    hashed = str(hashed)[2:-1]
    return hashed
