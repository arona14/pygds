from pygds.core.sessions import SessionInfo


class GdsResponse:
    """
    This class is for holding a parsed response from GDS. It will include the session information and the useful data (payload)
    """

    def __init__(self, session_info: SessionInfo, payload=None):
        self.session_info = session_info
        self.payload = payload
