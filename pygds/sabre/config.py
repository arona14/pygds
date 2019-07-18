# This file will be change for refactoring purpose.

import base64


conn = {}

credentials = {
    "WR17": {}
}


def sabre_credentials(pcc):
    try:
        return credentials[pcc]
    except KeyError:
        return None


def decode_base64(source):
    return base64.b64decode(source).decode('utf-8')


def encode_base64(source):
    return base64.b64encode(source.encode('utf-8')).decode("utf-8")


def main():
    pass


if __name__ == '__main__':
    main()
