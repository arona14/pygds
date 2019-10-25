from datetime import datetime


class SessionInfo:
    """
    This class is for containing information for a session
    """
    def __init__(self, security_token: str, sequence_number: int, session_id: str, message_id: str,
                 session_ended: bool = True):
        self.security_token = security_token
        self.sequence_number = sequence_number
        self.session_id = session_id
        self.message_id = message_id
        self.session_ended = session_ended
        self.last_access: datetime = None

    def __repr__(self):
        return str(self.__data())

    def __data(self):
        return {
            "security_token": self.security_token,
            "sequence_number": self.sequence_number,
            "session_id": self.session_id,
            "message_id": self.message_id,
            "session_ended": self.session_ended,
            "last_access": self.last_access
        }

    def __str__(self):
        return str(self.__data())


class SessionHolder(object):
    """
        This class is for holding information for sessions.
        The real use case is that we don't really need to hold all the info, but just the message id.

    """
    def __init__(self):
        self.current_sessions = {}

    def add_session(self, session_info: SessionInfo) -> None:
        """
            Add a new session object to the holder.
        """
        if session_info is None:
            raise ValueError("The session info cannot be null")
        self.current_sessions[session_info.message_id] = session_info

    def get_session_info(self, message_id: str) -> SessionInfo:
        """
            Get the session object by giving the message id
        """
        try:
            return self.current_sessions[message_id]
        except KeyError:
            return None

    def remove_session(self, message_id: str) -> None:
        """
            Remove a session by giving it's message id
        """
        if self.contains_session(message_id):
            del self.current_sessions[message_id]

    def update_session_sequence(self, message_id: str, sequence_number: int) -> None:
        """
            Update the sequence number of a session
        """
        if self.contains_session(message_id):
            self.current_sessions[message_id].sequence_number = sequence_number

    def contains_session(self, message_id: str) -> bool:
        """
            Tells weather the holder contains a message id or not.
        """
        return self.current_sessions.__contains__(message_id)
