from .amadeus_types import AmadeusSessionInfo


class SessionHolder(object):
    """
        This class is for holding information for sessions.
        The real use case is that we don't really need to hold all the info, but just the session id.

    """
    def __init__(self):
        self.current_sessions = {}

    def add_session(self, session_info: AmadeusSessionInfo):
        """
            Add a new session object to the holder.
        """
        if session_info is None:
            raise ValueError("The session info cannot be null")
        self.current_sessions[session_info.session_id] = session_info

    def get_session_info(self, session_id: str):
        """
            Get the session object by giving the session id
        """
        return self.current_sessions[session_id]

    def remove_session(self, session_id: str):
        """
            Removea a session by giving it's session id
        """
        if self.contains_session(session_id):
            del self.current_sessions[session_id]

    def update_session_sequence(self, session_id: str, sequence_number: int):
        """
            Update the sequence number of a session
        """
        if self.contains_session(session_id):
            self.current_sessions[session_id].sequence_number = sequence_number

    def contains_session(self, session_id: str):
        """
            Tells wehter the holder contains a session id or not.
        """
        return self.current_sessions.__contains__(session_id)
