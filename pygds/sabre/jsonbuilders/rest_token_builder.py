from pygds.core.security_utils import encode_base64

FORMAT_VERSION = "V1"
DOMAIN = "AA"


def build_sabre_new_rest_token_header(pcc: str, username: str, password: str):
    credentials = f"{FORMAT_VERSION}:{username}:{pcc}:{DOMAIN}"
    secret = encode_base64(password)
    return encode_base64(encode_base64(credentials) + ":" + secret)
