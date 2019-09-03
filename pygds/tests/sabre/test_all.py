"""
    This is for testing purposes like a suite.
"""

from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


def test():
    """ A suite of tests """

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"

    client = SabreClient(url, "", username, password, pcc, False)

    request = {
        "passengers": [
            {
                "first_name": "BABACAR",
                "last_name": "NDIAYE",
                "name_number": "01.01",
                "ticket_number": "0167452785035"
            }
        ],
        "segments": [
            {
                "departure_airport": "DTW",
                "arrival_airport": "ORD",
                "departure_date_time": "2019-10-11"
            },
            {
                "departure_airport": "ORD",
                "arrival_airport": "CDG",
                "departure_date_time": "2019-10-11"
            }
        ]
    }

    display_pnr = client.get_reservation("QZRFYZ ", None)
    # is_ticket = client.is_ticket_exchangeable(display_pnr.session_info.message_id, "0167452785035")
    sabre_command = client.exchange_shopping(display_pnr.session_info.message_id, "QZRFYZ", request["passengers"], request["segments"])
    return sabre_command


if __name__ == "__main__":
    print(test())
