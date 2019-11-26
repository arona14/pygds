"""
    This is for testing purposes like a suite.
"""

import os
import re
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting
from pygds import log_handler


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
    pnr = "Q698UG"
    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)

    try:
        token = None
        res_reservation = client.get_reservation(pnr, token, False)
        session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        if session_info.session_ended is True:
            log.error(" Session is ended after retrieve PNR")
        message_id = session_info.message_id
        ticket_number = [t.time for t in res_reservation["ticketing_info"]]
        list_ticket_number = []
        list_ticket = []
        void_response = None
        for ticket in ticket_number:
            if len(ticket):
                list_ticket.append(ticket)
                ticket_number = re.split("[, -/. ]+", ticket)
                t_number1 = ticket_number[1]
                t_number2 = ticket_number[2]
                list_ticket_number.append(t_number1 + t_number2)

        void_response = client.void_tickets(message_id, [list_ticket_number[0]] if len(list_ticket_number) else [])
        session_info, void_response = (void_response.session_info, void_response.payload)
        if session_info.session_ended is False:
            client.close_session(message_id)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
