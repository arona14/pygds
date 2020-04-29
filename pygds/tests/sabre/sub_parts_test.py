import unittest
from pygds.sabre.xmlbuilders.sub_parts import get_commision, get_fare_type, get_passenger_type, get_segment_number, \
    get_markup_exchange_price, get_commission_exchange, get_form_of_payment

passenger_type = [
    {
        "code": "JCB",
        "name_select": [
            "01.01"
        ],
        "quantity": 1
    },
    {
        "code": "JCB",
        "name_select": [
            "02.01"
        ],
        "quantity": 1
    },
    {
        "code": "J11",
        "name_select": [
            "03.01"
        ],
        "quantity": 1
    },
    {
        "code": "JNF",
        "name_select": [
            "04.01"
        ],
        "quantity": 1
    }
]


class SubPartsTest(unittest.TestCase):
    def test_get_commision(self):
        result = get_commision(0, 'WR17', 'abc')
        self.assertEqual(result, "")

    def test_get_fare_type(self):
        result = get_fare_type("Net")
        self.assertIsNone(result)

    def test_get_passenger_type(self):
        result = get_passenger_type(passenger_type, 'Net')
        self.assertIsNotNone(result)

    def test_get_segment_number(self):
        segment_select = [1, 2, 3, 4]
        result = get_segment_number(segment_select)
        a = "<ItineraryOptions><SegmentSelect Number='1'/><SegmentSelect Number='2'/><SegmentSelect Number='3'/><SegmentSelect Number='4'/></ItineraryOptions>"
        self.assertEqual(result, a)

    def test_markup_exchange_price(self):
        result = get_markup_exchange_price(30)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, str))
        self.assertIn("PlusUp", result)

    def test_commission_exchange(self):
        fare_type_net = get_commission_exchange("NET", 10)
        self.assertIsNotNone(fare_type_net)
        self.assertTrue(isinstance(fare_type_net, str))
        self.assertIn("MiscQualifiers", fare_type_net)
        fare_type_pub = get_commission_exchange("PUB", 10)
        self.assertTrue(isinstance(fare_type_pub, str))
        self.assertIn("MiscQualifiers", fare_type_pub)
        self.assertIsNotNone(fare_type_pub)

    def test_form_of_payment(self):
        form_of_payment = get_form_of_payment("CC", "AX", "2023", "111111111111")
        self.assertTrue(isinstance(form_of_payment, str))
        self.assertIsNotNone(form_of_payment)


if __name__ == "__main__":
    unittest.main()
