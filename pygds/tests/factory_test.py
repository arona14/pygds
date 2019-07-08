# factory.py test file
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import unittest
import pygds.factory as factory
from pygds.sabre.sabre_gds import SabreGDS
from pygds.amadeus.amadeus_gds import AmadeusGDS
from pygds.sabre.FormatSoapSabre import FormatSoapSabre


class TestFactory(unittest.TestCase):
    def test_factory_registration(self):
        print(SabreGDS)
        print(AmadeusGDS)
        #self.assertIsNotNone(factory.GDS('sabre').get_reservation('YQZMVU', 'WR17', 'factory-test-pygds'))
        objet_data = FormatSoapSabre().get_segment(self.assertIsNotNone(factory.GDS('sabre').get_reservation('YQZMVU', 'WR17', 'factory-test-pygds')))
        return objet_data

        
if __name__ == '__main__':
    unittest.main()
