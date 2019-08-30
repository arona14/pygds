"""
    This is for testing purposes like a suite.
"""
import os
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
# from pygds.core.request import TravellerNumbering, LowFareSearchRequest, RequestedSegment


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    # log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    # log = log_handler.get_logger("test_all")

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"

    rest_url = "https://api.havail.sabre.com"

    client = SabreClient(url, rest_url, username, password, pcc, False)
    return client
    """
    segment_select = [1, 2, 3, 4]
    passenger_type = [
        {
            "code": "JCB",
            "nameSelect": [
                "01.01"
            ],
            "quantity": 1
        },
        {
            "code": "JCB",
            "nameSelect": [
                "02.01"
            ],
            "quantity": 1
        },
        {
            "code": "J11",
            "nameSelect": [
                "03.01"
            ],
            "quantity": 1
        },
        {
            "code": "JNF",
            "nameSelect": [
                "04.01"
            ],
            "quantity": 1
        }
    ]
    display_pnr = client.get_reservation("XCVYRX", None)
    session_info = display_pnr.session_info
    if not session_info:
        print("Awma session info")
        return
    message_id = session_info.message_id
    price = client.search_price_quote(message_id, retain=False, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type)
    print(price)
    """
