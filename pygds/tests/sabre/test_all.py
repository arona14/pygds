"""
    This is for testing purposes like a suite.
"""
import os
import jxmlease
import json
import requests

from pygds.core.helpers import get_data_from_xml
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds import log_handler
from pygds.sabre.client import SabreClient
from pygds import log_handler

from pygds.core.request import LowFareSearchRequest, TravellerNumbering, RequestedSegment


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    log = log_handler.get_logger("test_all")

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # log = log_handler.get_logger("test_all")
    # pnr = "RH3WOD"  # "Q68EFX", "RI3B6D", "RT67BC"
    # m_id = None

    #urlpattern = "https://api.havail.sabre.com" + "/v4.1.0/shop/flights?mode=live"

    rest_url = "https://api.havail.sabre.com"

    client = SabreClient(url, rest_url, username, password, pcc, False)
    # try:
    segment1 = RequestedSegment("ATH", "LHR", "2019-09-17").to_data()
    segment2 = RequestedSegment("LHR", "ATH", "2019-09-26").to_data()

    segments = []
    segments.append(segment1)
    segments.append(segment2)

    travel_number = TravellerNumbering(1, 0, 0)

    print(travel_number.to_data())
    my_request = LowFareSearchRequest(segments, "Y", "WR17", travel_number, [], "50ITINS", [], False, False, 2)
    # print(my_request.to_data())
    # log.info(session_response)
    # except ClientError as ce:
    # log.error(f"client_error: {ce}")
    # log.error(f"session: {ce.session_info}")
    # except ServerError as se:
    # log.error(f"server_error: {se}")
    # log.error(f"session: {se.session_info}")
    """ 
        Test Search Flight Sabre 
    """
    response = client.search_flightrq("Modou", my_request, "NET")
    response = json.loads(response.content)
    #client.search_flightrq(None, my_request, "PUB")
    return response

    

if __name__ == "__main__":
    result = test()
    result = json.dumps(dict(result), sort_keys=False, indent=4)
    with open("myResult.json", 'w') as myFile:
        myFile.write(str(result))
    myFile.close()
