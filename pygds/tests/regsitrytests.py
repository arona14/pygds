from unittest import TestCase
from pygds.gdsregistry import GDSRegistry

class RegisterTest(TestCase):

    def test_instanciate(self):
        inst = GDSRegistry()
        self.assertIsNotNone(inst, "The instance is None")

    def test_singleton(self):
        inst1 = GDSRegistry()
        inst2 = GDSRegistry()
        self.assertEqual(inst1, inst2, "The two instances are not the same")