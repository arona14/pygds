from pygds.amadeus.amadeus_types import AmadeusSessionInfo
from ..errors.gdserrors import GDSError


class ClientError(GDSError):
    """
        A class to represent all exceptions from client side
    """
    def __init__(self, session_info: AmadeusSessionInfo, status_code, error_message):
        super(ClientError, self).__init__(session_info, "CLIENT_ERROR", error_message)
        self.status_code = status_code


class ServerError(GDSError):
    """
        A class to represent all exceptions from server side
    """
    def __init__(self, session_info: AmadeusSessionInfo, status_code, error_code, error_message):
        super(ServerError, self).__init__(session_info, error_code, error_message)
        self.status_code = status_code
