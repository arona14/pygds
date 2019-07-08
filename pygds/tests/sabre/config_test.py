# sabre config.py test file

import unittest
from pygds.sabre import config


class TestConfig(unittest.TestCase):
    def test_connection_ok(self):
        self.assertIsNotNone(config.conn)

    def test_sabre_credentials(self):
        res = config.sabre_credentials('WR17')
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
