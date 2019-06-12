from unittest import TestCase

from pygds.main import GDS

class TestMain(TestCase):
    # Just wanted to make sure that the function is accessible
    # These tests will be changed to real tests
    def test_get_reservation_ok(self):
        result = GDS.get_reservation('sabre', 'abc123', 'wr17', 'test')
        self.assertTrue(isinstance(result, str))

    def test_send_command_ok(self):
       
        result = GDS().send_command('sabre', '*JUBGEV','WR17', conversation_id='cosmo-material-b6851be0-b83e-11e8-be20-c56b920f05b5')
        self.assertTrue(isinstance(result,str))
