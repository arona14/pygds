import unittest
from pygds.sabre.xmlbuilders.sub_parts import get_commision, get_fare_type, get_passenger_type, get_segment_number

passenger_type = [
    {
        "code": "JCB",
        "nameSelect": [
            "01.01"
        ],
        "quantity": 1
    },
    {
        "code": "JCB",
        "nameSelect": [
            "02.01"
        ],
        "quantity": 1
    },
    {
        "code": "J11",
        "nameSelect": [
            "03.01"
        ],
        "quantity": 1
    },
    {
        "code": "JNF",
        "nameSelect": [
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


if __name__ == "__main__":
    unittest.main()
