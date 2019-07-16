# This file will be change for refactoring purpose.

import base64
import pandas as pd


def sabre_credentials(pcc):

    credentials = None
    try:
        query = f"""select "User","Password1" from portal_sabrecredentials where "Pcc" ='{pcc}' """
        if query is not None:
            credentials = pd.read_sql(sql=query, con=None)
    except:
        # TODO: Capture the real exception not the general one
        pass
    return credentials


def decode_base64(source):
    return base64.b64decode(source).decode('utf-8')


def encode_base64(source):
    return base64.b64encode(source.encode('utf-8')).decode("utf-8")


def main():
    pass


if __name__ == '__main__':
    main()
