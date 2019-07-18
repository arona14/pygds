import os
from unittest import TestCase

from pygds.amadeus.client import AmadeusClient
from pygds.env_settings import get_setting
from pygds import log_handler


class ClientCan(TestCase):
    def setUp(self) -> None:
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        self.client = AmadeusClient(endpoint, username, password, office_id, wsap, True)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        log_handler.load_file_config(os.path.join(dir_path, "..", "..", "..", "log_config.yml"))
        self.log = log_handler.get_logger("client_test")

    def send_command(self):
        s_id, seq, tok, m_id = (None, None, None, None)
        pnr = "Q68EFX"
        res_command = self.client.send_command(f"RT{pnr}", m_id, s_id, seq, tok)
        self.assertIsNotNone(res_command, "The result of send command is none")
        session_info, command_response = (res_command.session_info, res_command.payload)
        self.assertIsNotNone(session_info, "The session information is none")
        self.assertIsNotNone(command_response, "The result of send command is none")
