from errors.gdserrors import GDSError


class ClientError(GDSError):
    def __init__(self, status_code, error_message):
        super(ServerError, self).__init__("CLIENT_ERROR", error_message)
        self.status_code = status_code


class ServerError(GDSError):
    def __init__(self, status_code, error_code, error_message):
        super(ServerError, self).__init__(error_code, error_message)
        self.status_code = status_code
