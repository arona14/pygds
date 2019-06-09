from unittest import TestCase

from pygds.sabre.config import conn

class TestDB(TestCase):
    def test_connection_ok(self):
        self.assertIsNotNone(conn)