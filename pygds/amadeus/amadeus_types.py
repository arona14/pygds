from pygds.core.app_error import ApplicationError
from pygds.core.sessions import SessionInfo


class GdsResponse:
    """
    This class is for holding a parsed response from GDS. It will include the session information and the useful data (payload)
    """

    def __init__(self, session_info: SessionInfo, payload=None, app_error: ApplicationError = None):
        self.session_info = session_info
        self.payload = payload
        self.application_error = app_error

    def to_dict(self):
        return {
            "session_info": None if not self.session_info else self.session_info.__str__(),
            "payload": str(self.payload),
            "application_error": self.application_error.to_dict() if self.application_error else None
        }

    def __str__(self):
        return str(self.to_dict())
