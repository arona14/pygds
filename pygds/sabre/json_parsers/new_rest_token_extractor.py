import datetime
import json

from pygds.core.client import RestToken


def extract_sabre_rest_token(text: str):
    data = json.loads(text)
    token = data["access_token"]
    expires_in = data["expires_in"]
    return RestToken(token, datetime.datetime.now() + datetime.timedelta(seconds=expires_in))
