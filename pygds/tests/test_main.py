from unittest import TestCase

from pygds.main import get_reservation

class TestMain(TestCase):
    def test_get_reservation_ok(self):
        result = get_reservation('sabre', 'abc123', 'wr17', 'test')
        self.assertTrue(isinstance(result, str))
