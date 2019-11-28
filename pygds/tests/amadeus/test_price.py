import unittest
from pygds.amadeus.price import InformativeFareTax, TaxInformation, OptionDetail


class TestPrice(unittest.TestCase):
    """
    This class will test all function in the client side
    """
    def test_OptionDetail(self):
        result = OptionDetail(None, [], []).to_data()
        self.assertIsNotNone(result)

    def test_ift(self):
        result = InformativeFareTax(None, None, None, None).to_data()
        self.assertIsNotNone(result)

    def test_tax_information(self):
        result = TaxInformation([]).to_data()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
