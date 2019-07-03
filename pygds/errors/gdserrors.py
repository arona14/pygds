class GDSError(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.__repr__()


class GDSNotFoundError(GDSError):
    def __init__(self, gds_code):
        super(GDSNotFoundError, self).__init__("GDS_NOT_FOUND_ERROR", f"GDS with code {gds_code} not found in the resgistry.")
        self.gds_code = gds_code
