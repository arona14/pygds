import jwt
import datetime
from pygds.env_settings import get_setting

TOKEN_KEY = get_setting("SECRET_KEY")
ALGORITHM_TYPE = get_setting("ALGORYTHM_TOKEN")
DURATION = get_setting("DURATION_TOKEN")


def generate_token(message_id: str, sequence: int, session_id: str, security_token: str):
    """
    This method generate a token by giving him these parameters
    param message_id: the message_id
    param sequence: the sequance_number
    param session_id: the session_id
    param security_token: the security_token
    return token
    """
    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(DURATION)),
         "info_token": {"message_id": f"""{message_id}""",
                        "sequence": f"""{sequence}""", "session_id": f"""{session_id}""",
                        "security_token": f"""{security_token}"""}}, TOKEN_KEY, ALGORITHM_TYPE)
    return token


def decode_token(token: str):
    print("*** Test Token***")
    print(type(token))
    if token is None:
        return None
    try:
        return jwt.decode(token, TOKEN_KEY, ALGORITHM_TYPE)
    except jwt.ExpiredSignatureError:
        return None
