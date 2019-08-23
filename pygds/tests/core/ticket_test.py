import unittest
from pygds.core.ticket import TicketReply


class TypeHelpersTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def test_ticket_reply(self):
        result = TicketReply(None, None, None, None, None, None).to_dict()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
