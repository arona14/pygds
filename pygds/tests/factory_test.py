# factory.py test file
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import unittest
import pygds.factory as factory
from pygds.amadeus.amadeus_gds import AmadeusGDS


class TestFactory(unittest.TestCase):
    def test_factory_registration(self):
        print(AmadeusGDS)
        self.assertIsNotNone(factory.GDS('amadeus').get_reservation('YQZMVU', 'WR17', 'factory-test-pygds'))


if __name__ == '__main__':
    unittest.main()
