class CreatePnrInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class CreatePnrInfo(CreatePnrInfoBasic):

    def __init__(self):
        self.status: str = None  # the response status
        self.itinerary_ref: dict = None  # the itinerary ref (record id)
        self.air_book: dict = None  # the airbook response
        self.air_price: dict = None  # the air price response
        self.travel_itinerary_read: dict = None  # the travel itinerary

    def to_dict(self):
        return {
            "Status": self.status,
            "RecordLocator": self.itinerary_ref,
            "AirBook": self.air_book,
            "AirPrice": self.air_price,
            "TravelItineraryRead": self.travel_itinerary_read
        }
