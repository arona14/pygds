import os
from pygds.amadeus.client import AmadeusClient
from pygds.core.price import PriceRequest
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting
from pygds.core.helpers import ensure_list
from pygds import log_handler
import fnc


def test():
    """ A suite of tests """
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    log = log_handler.get_logger("test_all")
    pnr = "MYXH99"  # Q7N3A8 O95J97 WY9R4Z JSUDTM TTX3QV JSUDTM

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)

    try:
        token = None
        res_reservation = client.get_reservation(token, False, pnr)

        session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        pax_refs = []
        seg_refs = []
        for pax in ensure_list(fnc.get("passengers", res_reservation, default=[])):
            pax_refs.append(pax.name_id)
        for segs in ensure_list(fnc.get("itineraries", res_reservation, default=[])):
            for seg in ensure_list(fnc.get("segments", segs, default=[])):
                seg_refs.append(seg.sequence)
        request_price = PriceRequest(pax_refs, seg_refs, "OTHER", 0, "")
        log.debug("result of price_request")
        log.debug(request_price)
        token = session_info.security_token
        res_price = client.fare_price_pnr_with_booking_class(token, request_price)
        log.debug(res_price)

        if session_info.session_ended is False:
            client.close_session(token)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
