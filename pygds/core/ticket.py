from pygds.core.price import PriceInfoBasic


class TicketReply(PriceInfoBasic):

    def __init__(self, status: str, error_code, qualifier, source, encoding, description):
        self.status = status
        self.error_code = error_code
        self.qualifier = qualifier
        self.source = source
        self.encoding = encoding
        self.description = description
        self.is_error = status == "X"
        self.is_warning = status == "W"
        self.is_ok = status == "O"

    def to_dict(self):
        return {
            "status": self.status,
            "error_code": self.error_code,
            "qualifier": self.qualifier,
            "source": self.source,
            "encoding": self.encoding,
            "description": self.description,
            "is_error": self.is_error,
            "is_warning": self.is_warning,
            "is_ok": self.is_ok
        }
