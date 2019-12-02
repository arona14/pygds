import jwt
import datetime
from pygds.core.config import JWT_ALGORYTHM_TOKEN_AMADEUS, JWT_DURATION_TOKEN_AMADEUS, JWT_SECRET_KEY_AMADEUS


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
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_DURATION_TOKEN_AMADEUS)),
         "info_token": {"message_id": f"""{message_id}""",
                        "sequence": f"""{sequence}""", "session_id": f"""{session_id}""",
                        "security_token": f"""{security_token}"""}}, JWT_SECRET_KEY_AMADEUS, JWT_ALGORYTHM_TOKEN_AMADEUS)
    return token


def decode_token(token: str):
    if token is None:
        return None
    try:
        return jwt.decode(token, JWT_SECRET_KEY_AMADEUS, JWT_ALGORYTHM_TOKEN_AMADEUS)
    except jwt.ExpiredSignatureError:
        return None
