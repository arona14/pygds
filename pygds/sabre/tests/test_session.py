from unittest import TestCase

from pygds.sabre.session import SabreSession


class TestSession(TestCase):
    def test_session_open(self):
        token = SabreSession().open('WR17', 'test')
        self.assertTrue(isinstance(token, str))
