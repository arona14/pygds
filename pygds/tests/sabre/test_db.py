from unittest import TestCase

from pygds.sabre.config import conn, sabre_credentials


class TestDB(TestCase):
    def test_connection_ok(self):
        self.assertIsNotNone(conn)

    def test_sabre_credentials(self):
        res = sabre_credentials('WR17')
        self.assertIsNotNone(res)


