from unittest import TestCase
import requests
from pygds.tests.sabre.variables_of_tests import pcc_, pnr_, conversation_id_
from pygds.sabre.reservation import SabreReservation
from pygds.sabre.session import SabreSession, SabreXMLBuilder


class TestGetReservation(TestCase):

    def setUp(self):
        self.pnr = pnr_
        self.pcc = pcc_
        self.conversation_id = conversation_id_

    def test_get_is_ok(self):
        result = SabreReservation().get(self.pnr, self.pcc, self.conversation_id)
        self.assertIsNotNone(result)
