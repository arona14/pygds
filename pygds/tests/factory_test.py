# factory.py test file

from unittest import TestCase
from pygds.factory import GDS


class TestFactory(TestCase):
    def test_factory_registration(self):
        self.assertIsNotNone(GDS('sabre').get_reservation('YQZMVU'))
        self.assertTrue(isinstance(GDS('amadeus').get_reservation('YQZMVU'), str))
