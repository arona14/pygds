from unittest import TestCase
import requests
from pygds.tests.sabre.variables_of_tests import gds_, pcc_, pnr_, conversation_id_, token_, url_, headers_
from pygds.sabre.reservation import SabreReservation
from pygds.sabre.session import SabreSession, SabreXMLBuilder


class TestGetReservation(TestCase):

    def setUp(self):
        self.gds = gds_
        self.pnr = pnr_
        self.pcc = pcc_
        self.conversation_id = conversation_id_
        self.token = token_
        self.url = url_
        self.headers = headers_

    def test_get_is_ok(self):
        token_result = SabreSession().open(self.pcc, self.conversation_id)
        request_builder_result = SabreXMLBuilder().getReservationRQ(
            self.pcc, self.conversation_id, self.token, self.pnr)
        api_response = requests.post(
            self.url, data=request_builder_result, headers=self.headers)
        result = SabreReservation().get(self.pnr, self.pcc, self.conversation_id)
        self.assertTrue(isinstance(token_result, str))
        self.assertTrue(isinstance(request_builder_result, str))
        self.assertTrue(isinstance(api_response, object))
        self.assertTrue(isinstance(result, object))
