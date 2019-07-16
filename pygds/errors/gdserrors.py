from pygds.amadeus.amadeus_types import AmadeusSessionInfo


class GDSError(Exception):
    def __init__(self, session_info: AmadeusSessionInfo, error_code: str, error_message: str):
        self.session_info = session_info
        self.error_code = error_code
        self.error_message = error_message

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.__repr__()


class GDSNotFoundError(GDSError):
    def __init__(self, gds_code):
        super(GDSNotFoundError, self).__init__(None, "GDS_NOT_FOUND_ERROR", f"GDS with code {gds_code} not found in the resgistry.")
        self.gds_code = gds_code
