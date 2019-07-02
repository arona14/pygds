# This file will be change for refactoring purpose.

import psycopg2
import base64
import pandas as pd

fterospostgres = {
    "host": "ec2-174-129-227-51.compute-1.amazonaws.com",
    "user": "fbxukujmusdgza",
    "pwd": "8b831e68c329940e8a9d66cbd9219d286785a59bad4af76562c536bac3c1207d",
    "db": "d7nsrrkmige2hd"
}

try:
    conn = psycopg2.connect(
        f"""host={fterospostgres["host"]} dbname={fterospostgres["db"]} user={fterospostgres["user"]} password={fterospostgres["pwd"]}""")
except:
    # TODO: Capture the real exception not the general one
    conn = None


def sabre_credentials(pcc):

    credentials = None
    try:
        query = f"""select "User","Password1" from portal_sabrecredentials where "Pcc" ='{pcc}' """
        if query is not None:
            credentials = pd.read_sql(sql=query, con=conn)
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
