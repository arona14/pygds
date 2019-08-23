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

    client = SabreClient(url, username, password, pcc, False)

    segment_select = [1, 2, 3]
    passenger_type = {
        "code": "JCB", "markup": 0, "commissionPercentage": None, "nameSelect": "01.01", "tourCode": None, "ticketDesignator": None, "serviceFee": None, "proposed": 707.43, "quantity": 1
    }

    brand_id = None
    display_pnr = client.get_reservation("KHIDYK", None)
    session_info = display_pnr.session_info
    if not session_info:
        print("Awma session info")
        return
    message_id = session_info.message_id
    # price = client.search_price_quote(message_id, retain=False, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type)
    store_price = client.store_price_quote(message_id, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type, brand_id=brand_id)
    print(store_price)


if __name__ == "__main__":
    test()
