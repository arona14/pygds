import uuid
from time import gmtime, strftime
import secrets
import base64


def generate_random_message_id(prefix: str = ""):
    return prefix + str(uuid.uuid4())


def generate_nonce(nBytes=16):
    """
    This method generates a nonce value and base64 encode it
    """
    nonce = base64.encodebytes(secrets.token_bytes(nBytes))
    return str(nonce)[2:-3]


def generate_created():
    # 2017-05-29T14:44:41.457Z
    return str(strftime("%Y-%m-%dT%H:%M:%S.%ZZ", gmtime()))


def main():
    nonce = generate_nonce()
    messageId = generate_random_message_id()
    print(f"none: {nonce}")
    print(f"messageId: {messageId}")
    created = generate_created()
    print(f"created: {created}")


if __name__ == "__main__":
    main()
