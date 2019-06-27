# factory.py test file

from unittest import TestCase
from pygds.factory import GDS
from pygds.sabre.sabre_gds import SabreGDS
from pygds.amadeus.amadeus_gds import AmadeusGDS


class TestFactory(TestCase):
    def test_factory_registration(self):

        print(SabreGDS)
        print(AmadeusGDS)
        self.assertIsNotNone(GDS('sabre').get_reservation('YQZMVU', 'WR17', 'factory-test-pygds'))
