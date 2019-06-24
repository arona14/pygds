class GDSError(Exception):
    pass

class GDSNotFoundError(GDSError):
    def __init__(self, gds_code):
        self.gds_code = gds_code

    def __repr__(self):
        return f"GDS with code {self.gds_code} not found in the resgistry."
    def __str__(self):
        return self.__repr__()