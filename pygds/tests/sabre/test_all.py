"""
    This is for testing purposes like a suite.
"""
import os
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


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

    client = SabreClient(url, "", username, password, pcc, False)

    segment_select = [1, 2, 3, 4]
    passenger_type = {
        "code": "ADT",
        "nameSelect": "01.01",
        "firstName": "DEMBA",
        "lastName": "NDIAYE",
        "birthDate": "1984-07-13",
        "gender": "M",
        "markup": 0,
        "commissionPercentage": 10,
        "tourCode": "815ZU",
        "ticketDesignator": "PP10",
        "serviceFee": 0,
        "baseFare": 26,
        "totalFare": 371.93,
        "paxType": "ADT",
        "proposed": 371.93,
        "creditCard": None,
        "quantity": 1
    }
    # passenger_type_price = [{"code": "ADT", "nameSelect": ["01.01"], "quantity":1}]
    brand_id = None
    display_pnr = client.get_reservation("WOHOIJ", None)
    session_info = display_pnr.session_info
    if not session_info:
        print("No session info")
        return
    message_id = session_info.message_id
    # price = client.search_price_quote(message_id, retain=False, fare_type='Pub', segment_select=segment_select, passenger_type=passenger_type_price)
    store_price = client.store_price_quote(message_id, retain=True, fare_type='Pub', segment_select=segment_select, passenger_type=passenger_type, brand_id=brand_id)
    print(store_price)


if __name__ == "__main__":
    test()
