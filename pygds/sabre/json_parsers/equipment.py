class AircraftInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class AircraftInfo(AircraftInfoBasic):

    def __init__(self):
        self.air_craft_info: list = []  # the travel itinerary

    def to_dict(self):
        return {
            "AircraftInfo": self.air_craft_info
        }
