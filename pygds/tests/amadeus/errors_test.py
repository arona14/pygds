from unittest import TestCase

from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.sessions import SessionInfo


class ErrorsTest(TestCase):
    def setUp(self) -> None:
        self.session_info = SessionInfo("SEC", 1, "SESS", "MESS", True)

    def test_client_error(self):
        c_error = ClientError(self.session_info, 404, "Not found")
        self.assertIsNotNone(c_error)
        self.assertEqual(c_error.status_code, 404)

    def test_server_error(self):
        s_error = ServerError(self.session_info, 502, "NO-PNR", "Not PNR")
        self.assertIsNotNone(s_error)
        self.assertEqual(s_error.status_code, 502)
