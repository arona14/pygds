"""
    This is for testing purposes like a suite.
"""
from pygds import log_handler
from pygds.env_settings import get_setting
import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
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
    log = log_handler.get_logger("test_all")
    client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
    pnr = "LC87DQ"
    try:

        message_id = None
        res_reservation = client.get_reservation(pnr, None, False)
        res_reservation, message_id = res_reservation.payload, res_reservation.session_info.message_id
        log.debug(" result reservation ")
        log.info(res_reservation)
        traveller_infos = [TravellerInfo(1, "Aliou", "Dianko", "Thiam", "03121990", "ADT"),
                           TravellerInfo(2, "Malick", "Serigne", "Ndiouck", "03121990", "ADT")]

        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")

        passenger_info_response = client.add_passenger_info(office_id, message_id, reservation_info)
        passenger_info_response, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
        if session_info.session_ended:
            log.error("Session is ended after creat pnr")

            return

        log.info("End of Calling Add Passenger Information ****************************************")

        log.info("begin  of Calling update Passenger Information ****************************************")
        res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, 2, "Diop", 2, "MOUHAMAD", "ADT", 1, "10JUN78")
        log.debug("update passenger")
        log.debug(res_updat_pas.payload)

        res_updat_pas1 = client.pnr_add_multi_for_pax_info_element(message_id, 1, "Ndiaye", 2, "Ibrahima", "ADT", 1, "10JUN78")
        log.debug("update passenger")
        log.debug(res_updat_pas1.payload)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
