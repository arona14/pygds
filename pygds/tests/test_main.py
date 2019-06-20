from unittest import TestCase
from pygds.main import GDS


class TestMain(TestCase):
    # Just wanted to make sure that the function is accessible
    # These tests will be changed to real tests
    def test_get_reservation_ok(self):
        result = GDS().get_reservation('sabre', 'JUBGEV', 'WR17', 'test')
        self.assertTrue(isinstance(result, object))

    def test_send_command_ok(self):
        result = GDS().send_command('sabre', '*JUBGEV', 'WR17', 'test')
        self.assertTrue(isinstance(result, object))

    def test_end_transaction_ok(self):
        result = GDS().end_transaction('sabre', 'WR17', 'test', 'test')
        self.assertTrue(isinstance(result, object))
