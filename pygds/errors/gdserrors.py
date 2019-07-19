from pygds.core.sessions import SessionInfo


class GDSError(Exception):
    """
        This is a base class for every error from GDS.
        It will take in account the session used.
    """
    def __init__(self, session_info: SessionInfo, error_code: str, error_message: str):
        """
        Initialization of a new GDSError
        :param session_info: the session info object
        :param error_code: the error code
        :param error_message: the error message
        """
        self.session_info = session_info
        self.error_code = error_code
        self.error_message = error_message

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.__repr__()


class GDSNotFoundError(GDSError):
    """
    An exception to raise when someone is trying to access a not existing GDS.
    """
    def __init__(self, gds_code):
        super(GDSNotFoundError, self).__init__(None, "GDS_NOT_FOUND_ERROR", f"GDS with code {gds_code} not found in the resgistry.")
        self.gds_code = gds_code
