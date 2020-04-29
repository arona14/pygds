import unittest
from pygds.amadeus.xmlbuilders.sub_parts import ppwbc_fare_type, ppwbc_discount, ticket_issue_tst_ref, \
    queue_place_target_queue, itc_pax_selection, itc_option_group


class SubPartsTest(unittest.TestCase):
    def test_fare_type(self):
        fare_type_net = ppwbc_fare_type("Net")
        fare_type_pub = ppwbc_fare_type("Pub")
        fare_type_com = ppwbc_fare_type("Pub")
        self.assertTrue(isinstance(fare_type_net, str))
        self.assertIsNotNone(fare_type_net)
        self.assertTrue(isinstance(fare_type_pub, str))
        self.assertIsNotNone(fare_type_pub)
        self.assertTrue(isinstance(fare_type_com, str))
        self.assertIsNotNone(fare_type_com)

    def test_ppwbc_discount(self):
        discount = ppwbc_discount()
        self.assertTrue(isinstance(discount, str))
        self.assertIsNotNone(discount)
        self.assertIn("discountInformation", discount)
        self.assertIn("penaltyType", discount)
        self.assertIn("discountCode", discount)

    def test_ticket_issue_tst_ref(self):
        issue_tst_ref = ticket_issue_tst_ref("40")
        self.assertTrue(isinstance(issue_tst_ref, str))
        self.assertIsNotNone(issue_tst_ref)
        self.assertIn("referenceDetails", issue_tst_ref)
        self.assertIn("type", issue_tst_ref)
        self.assertIn("value", issue_tst_ref)
        self.assertIn("</referenceDetails>", issue_tst_ref)

    def test_queue_place(self):
        queue_place = queue_place_target_queue("ABCD", "2", "1")
        self.assertTrue(isinstance(queue_place, str))
        self.assertIsNotNone(queue_place)
        self.assertIn("targetDetails", queue_place)
        self.assertNotIn("Virginie", queue_place)

    def test_pax_selection(self):
        pax_selection = itc_pax_selection("ADT")
        self.assertTrue(isinstance(pax_selection, str))
        self.assertIsNotNone(pax_selection)
        self.assertIn("paxSelection", pax_selection)
        self.assertIn("passengerReference", pax_selection)
        self.assertIn("type", pax_selection)
        self.assertIn("ADT", pax_selection)

    def test_option_group(self):
        option_group = itc_option_group("O")
        self.assertTrue(isinstance(option_group, str))
        self.assertIsNotNone(option_group)
        self.assertIn("optionGroup", option_group)
        self.assertIn("switches", option_group)
        self.assertIn("statusDetails", option_group)
        self.assertIn("</optionGroup>", option_group)
