from .price import PriceInfoBasic


class RebookInfo(PriceInfoBasic):

    def __init__(self):

        self.status: str  # response status
        self.air_book_rs: dict  # air book response
        self.travel_itinerary_read_rs: dict  # travel itinerary read response

    def to_dict(self):
        return {
            "Status": self.status,
            "AirBook": self.air_book_rs,
            "TravelItinerary": self.travel_itinerary_read_rs
        }
