"""
    This is for testing purposes like a suite.
"""
import os
import json
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
from pygds.core.request import RequestedSegment, LowFareSearchRequest, TravellerNumbering
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    # log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    # log = log_handler.get_logger("test_all")
    pcc = get_setting("SABRE_PCC")
    username = get_setting("SABRE_USERNAME")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    rest_url = "https://api.havail.sabre.com"
    soap_url = "https://webservices3.sabre.com"
    client = SabreClient(soap_url, rest_url, username, password, pcc, False)
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path_pub = os.path.join(base_path, "resources/sfjb/request_builder_pub.json")
    json_path_net = os.path.join(base_path, "resources/sfjb/request_builder_net.json")

    with open(json_path_pub) as j:
        search_pub = json.load(j)
    with open(json_path_net) as j:
        search_net = json.load(j)

    segment1 = RequestedSegment("DTW", "NYC", "2019-09-10").to_data()
    segment2 = RequestedSegment("NYC", "DTW", "2019-09-21").to_data()

    segments = []
    segments.append(segment1)
    segments.append(segment2)

    display_pnr = client.get_reservation("TLRYVS", None)
    session_info = display_pnr.session_info
    if not session_info:
        print("No session info")
        return
    message_id = session_info.message_id
    travel_number = TravellerNumbering(2, 1, 0)
    # token = session_info.security_token
    # price = client.search_price_quote(message_id, retain=False, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type)
    # print(price)
    # remark = client.send_remark(message_id, 'Virginie')
    # print(remark)
    # resul_ticket = client.issue_ticket(message_id, 1, code_cc=None, expire_date=None, cc_number=None, approval_code=None, payment_type="CK", commission_value=commission_value)
    # print(resul_ticket)
    # result = client.end_transaction(message_id)
    # print(result)
    my_request = LowFareSearchRequest(segments, "Y", "WR17", travel_number, [], "50ITINS", [], False, True, 2)
    result = client.search_flight(message_id, my_request, True, "PUB")
    print(result)


if __name__ == "__main__":
    test()
