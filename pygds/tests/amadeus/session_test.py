from unittest import TestCase
from pygds.amadeus.sessions import SessionHolder
from pygds.amadeus.amadeus_types import AmadeusSessionInfo


class SessionHolderCan(TestCase):

    def setUp(self):
        self.holder = SessionHolder()

    def init(self):
        holder = SessionHolder()
        self.assertIsNotNone(holder, "The created holder is none")

    def add_session(self):
        session_info = AmadeusSessionInfo("tok9999", 1, "fake-session-id", "pprrrr", "End")
        self.holder.add_session(session_info)
        self.assertTrue(self.holder.contains_session("fake-session-id"), "The holder didn't take the giving session")

    def get_session_info(self):
        session_info = AmadeusSessionInfo("tok9999", 1, "fake-session-id-2", "pprrrr", "End")
        self.holder.add_session(session_info)
        read_session = self.holder.get_session_info("fake-session-id-2")
        self.assertIsNotNone(read_session, "No session found in the holder")
        self.assertEqual("tok9999", read_session.session_id, "The token read doesn't match")

    def remove_session(self):
        session_info = AmadeusSessionInfo("tok9999", 1, "fake-session-id-3", "pprrrr", "End")
        self.holder.add_session(session_info)
        self.holder.remove_session("fake-session-id-3")
        self.assertFalse(self.holder.contains_session("fake-session-id-3"), "The session is not removed")

    def update_session_sequence(self):
        session_info = AmadeusSessionInfo("tok9999", 1, "fake-session-id-4", "pprrrr", "End")
        self.holder.add_session(session_info)
        self.holder.update_session_sequence("fake-session-id-4", 3)
        read_session = self.holder.get_session_info("fake-session-id-4")
        self.assertIsNotNone(read_session, "No session found in the holder")
        self.assertEqual(3, read_session.sequence_number, "The read sequence number doesn't match")

    def tell_contains_session(self):
        session_info = AmadeusSessionInfo("tok9999", 1, "fake-session-id-5", "pprrrr", "End")
        self.holder.add_session(session_info)
        contains = self.holder.contains_session("fake-session-id-5")
        self.assertTrue(contains, "The holder doesn't contain the added session")

    def tell_not_contains_session(self):
        contains = self.holder.contains_session("fake-session-id-999")
        self.assertFalse(contains, "The holder contains not added session")
