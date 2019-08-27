class Segment:

    def __init__(self):
        self.departure_date_time: str
        self.arrival_date_time: str
        self.flight_number: str
        self.res_book_desig_code: str
        self.status: str
        self.destination: str
        self.marketing_code: str
        self.operating_code: str
        self.origin: str
        self.number_in_party: str

    def to_dict(self):
        return {
            "departure_date_time": self.departure_date_time,
            "arrival_date_time": self.arrival_date_time,
            "flight_number": self.flight_number,
            "res_book_desig_code": self.res_book_desig_code,
            "status": self.status,
            "destination": self.destination,
            "marketing_code": self.marketing_code,
            "operating_code": self.operating_code,
            "origin": self.origin,
            "number_in_party": self.number_in_party
        }
