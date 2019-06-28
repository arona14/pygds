class AmadeusSessionInfo():
    """
    This class is for containing information for a session
    """
    def __init__(self, security_token, sequence_number, session_id, status_code):
        self.security_token = security_token
        self.sequence_number = sequence_number
        self.session_id = session_id
        self.status_code = status_code

    def is_ok(self):
        return self.status_code == 'P'
