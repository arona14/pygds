class AmadeusSessionInfo:
    """
    This class is for containing information for a session
    """
    def __init__(self, security_token, sequence_number, session_id):
        self.security_token = security_token
        self.sequence_number = sequence_number
        self.session_id = session_id

    def __repr__(self):
        return {
            "security_token": self.security_token,
            "sequence_number": self.sequence_number,
            "session_id": self.session_id
        }

    def __str__(self):
        return str(self.__repr__())