from unittest import TestCase

from pygds.main import get_reservation

class TestMain(TestCase):
    # Just wanted to make sure that the function is accessible
    # These tests will be changed to real tests
    def test_get_reservation_ok(self):
        result = get_reservation('sabre', 'abc123', 'wr17', 'test')
        self.assertTrue(isinstance(result, str))
