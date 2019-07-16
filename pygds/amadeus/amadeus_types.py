class AmadeusSessionInfo:
    """
    This class is for containing information for a session
    """
    def __init__(self, security_token: str, sequence_number: int, session_id: str, message_id: str, session_ended: str = True):
        self.security_token = security_token
        self.sequence_number = sequence_number
        self.session_id = session_id
        self.message_id = message_id
        self.session_ended = session_ended

    def __repr__(self):
        return {
            "security_token": self.security_token,
            "sequence_number": self.sequence_number,
            "session_id": self.session_id,
            "message_id": self.message_id,
            "session_ended": self.session_ended
        }

    def __str__(self):
        return str(self.__repr__())
