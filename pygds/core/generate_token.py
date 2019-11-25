import jwt
import datetime
from pygds.env_settings import get_setting

TOKEN_KEY = get_setting("SECRET_KEY")
ALGORITHM_TYPE = get_setting("ALGORYTHM_TOKEN")
DURATION = get_setting("DURATION_TOKEN")


def generate_token(message_id: str, sequence: int, session_id: str, security_token: str):

    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(DURATION)),
         "info_token": {"message_id": f"""{message_id}""",
                        "sequence": f"""{sequence}""", "session_id": f"""{session_id}""",
                        "security_token": f"""{security_token}"""}}, TOKEN_KEY, ALGORITHM_TYPE)
    return token


def decode_token(token: str):
    try:
        return jwt.decode(token, TOKEN_KEY, ALGORITHM_TYPE)
    except jwt.ExpiredSignatureError:
        return None
