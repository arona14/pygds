from unittest import TestCase
from pygds.core import security_utils


class SecurityUtilCan(TestCase):

    def setUp(self) -> None:
        self.su = security_utils

    def test_generate_random_message_id(self):
        rand_msg = self.su.generate_random_message_id()
        self.assertIsNotNone(rand_msg, "Cannot generate random message id")

    def test_generate_nonce(self):
        nonce = self.su.generate_nonce()
        self.assertIsNotNone(nonce, "Cannot generate nonce")

    def test_generate_created(self):
        created = self.su.generate_created()
        self.assertIsNotNone(created, "Cannot generate created")

    def test_normally_digest_message(self):
        nonce = self.su.generate_nonce()
        created = self.su.generate_created()
        password = "You have to ignore me"
        digested = self.su.password_digest(password, nonce, created)
        self.assertIsNotNone(digested, "Cannot digest the password")
        self.assertNotEquals(password, digested, "The digested password is same as the input")
