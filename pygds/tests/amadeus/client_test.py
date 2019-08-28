from unittest import TestCase
import unittest
from pygds.amadeus.client import AmadeusClient
from pygds.env_settings import get_setting
from pygds.errors.gdserrors import NoSessionError


class ClientCan(TestCase):
    def setUp(self) -> None:
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        self.client = AmadeusClient(endpoint, username, password, office_id, wsap, False)

    def test_send_command(self):
        seq, m_id = (None, None)
        pnr = "Q68EFX"
        res_command = self.client.send_command(f"RT{pnr}", m_id, seq)
        self.assertIsNotNone(res_command, "The result of send command is none")
        session_info, command_response = (res_command.session_info, res_command.payload)
        self.assertIsNotNone(session_info, "The session information is none")
        self.assertIsNotNone(command_response, "The result of send command is none")

    def test_end_session(self):
        res_command = self.client.send_command("HELP")
        self.assertIsNotNone(res_command)
        session = res_command.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)
        res_end_session = self.client.end_session(session.message_id)
        self.assertIsNotNone(res_end_session)
        session = res_end_session.session_info
        self.assertIsNotNone(session)
        self.assertTrue(session.session_ended)

    def test_end_session_not_exists(self):
        self.assertRaises(NoSessionError, self.client.end_session, "fake-message-id")


if __name__ == "__main__":
    unittest.main()
