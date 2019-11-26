import jwt
import datetime
# import time
from pygds.env_settings import get_setting
key = get_setting("AMADEUS_KEY")
algorithm = get_setting("AMADEUS_ALGORYTHM")
duration = int(get_setting("AMADEUS_DURATION"))


def generate_token(message_id: str, sequence: int, session_id: str, security_token: str):

    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=duration), "info_token": {"message_id": f"""{message_id}""", "sequence": f"""{sequence}""", "session_id": f"""{session_id}""", "security_token": f"""{security_token}"""}}, key, algorithm)
    return token


def decode_token(token: str):
    try:
        return jwt.decode(token, key, algorithm)
    except jwt.ExpiredSignatureError:
        return None


if __name__ == "__main__":
    token_encode = generate_token("uhgfueuhichi", 123444, "huhjebjbhb", "ihjjhjcjcb")
    # print(token_encode)
    # time.sleep(32)
    token_decode = decode_token(token_encode)
    print(token_decode["info_token"]["message_id"])
