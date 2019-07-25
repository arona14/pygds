from unittest import TestCase
from pygds.core.sessions import SessionInfo, SessionHolder


class SessionHolderCan(TestCase):

    def setUp(self):
        self.holder = SessionHolder()

    def test_init(self):
        holder = SessionHolder()
        self.assertIsNotNone(holder, "The created holder is none")

    def test_add_session(self):
        session_info = SessionInfo("tok9999", 1, "fake-session-id", "fake-message-id", True)
        self.holder.add_session(session_info)
        self.assertTrue(self.holder.contains_session("fake-message-id"), "The holder didn't take the giving session")

    def test_add_empty_session(self):
        self.assertRaises(ValueError, self.holder.add_session, None)  # "Adding empty session is not raising ValueError"

    def test_get_session_info(self):
        session_info = SessionInfo("tok9999", 1, "fake-session-id-2", "fake-message-id-2", False)
        self.holder.add_session(session_info)
        read_session = self.holder.get_session_info("fake-message-id-2")
        self.assertIsNotNone(read_session, "No session found in the holder")
        self.assertEqual("fake-session-id-2", read_session.session_id, "The token read doesn't match")

    def test_get_non_existing_session(self):
        ses = self.holder.get_session_info("no-sense-session")
        self.assertIsNone(ses, "session exists")

    def test_remove_session(self):
        session_info = SessionInfo("tok9999", 1, "fake-session-id-3", "fake-message-id-3", False)
        self.holder.add_session(session_info)
        self.holder.remove_session("fake-message-id-3")
        self.assertFalse(self.holder.contains_session("fake-message-id-3"), "The session is not removed")

    def test_update_session_sequence(self):
        session_info = SessionInfo("tok9999", 1, "fake-session-id-4", "fake-message-id-4", False)
        self.holder.add_session(session_info)
        self.holder.update_session_sequence("fake-message-id-4", 3)
        read_session = self.holder.get_session_info("fake-message-id-4")
        self.assertIsNotNone(read_session, "No session found in the holder")
        self.assertEqual(3, read_session.sequence_number, "The read sequence number doesn't match")

    def test_tell_contains_session(self):
        session_info = SessionInfo("tok9999", 1, "fake-session-id-5", "fake-message-id-5", True)
        self.holder.add_session(session_info)
        contains = self.holder.contains_session("fake-message-id-5")
        self.assertTrue(contains, "The holder doesn't contain the added session")

    def test_tell_not_contains_session(self):
        contains = self.holder.contains_session("fake-session-id-999")
        self.assertFalse(contains, "The holder contains not added session")
