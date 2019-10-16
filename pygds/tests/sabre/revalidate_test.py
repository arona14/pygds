"""
This is for testing purposes like a suite.
"""
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


def test():

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    rest_url = "https://api.havail.sabre.com"
    soap_url = "https://webservices3.sabre.com"
    client = SabreClient(soap_url, rest_url, username, password, pcc, False)
    retrieve_pnr = client.get_reservation("SKENNM", None, True)
    passengers = [
        {
            "code": "JCB",
            "quantity": 1
        }
    ]
    client.revalidate_itinerary(None, retrieve_pnr.payload["itineraries"], passengers, "Pub")


if __name__ == "__main__":
    test()
