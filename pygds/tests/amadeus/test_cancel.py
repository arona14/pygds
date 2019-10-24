"""
    This is for testing purposes like a suite.
"""

import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
# from pygds.core.payment import FormOfPayment, CreditCard
from pygds.core.price import PriceRequest  # , Fare
# from pygds.core.types import SellItinerary, TravellerNumbering, TravellerInfo
from pygds.env_settings import get_setting
from pygds import log_handler
from pygds.core.types import TravellerInfo, ReservationInfo


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
    log = log_handler.get_logger("test_cancel")
    pnr = "L6LMQP"  # "L6LMQP", "KDN6HQ", "Q68EFX", "Q68EFX", "RI3B6D", "RT67BC", "RH3WOD", "WKHPRE", "TSYX56", "SNG6IR", "SY9LBS"
    # m_id = None

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    # import web_pdb; web_pdb.set_trace()
    try:
        message_id = None
        res_reservation = client.get_reservation(pnr, message_id, False)
        session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        log.info(session_info)
        log.info(res_reservation)
        message_id = session_info.message_id
        # res_reservation = client.get_reservation(pnr, message_id, False)
        cancel_response = client.cancel_pnr(message_id, False)
        session_info, cancel_response = (cancel_response.session_info, cancel_response.payload)
        log.info(cancel_response)
        if session_info.session_ended is False:
            client.end_session(message_id)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
