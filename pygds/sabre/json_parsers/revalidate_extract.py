class RevalidateItinerarieInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class RevalidateItinerarieInfo(RevalidateItinerarieInfoBasic):

    def __init__(self):
        self.status: str = None  # status response
        self.brand_feature: dict = None  # brand_feature response
        self.priced_itinerarie: dict = None  # priced_itinerarie response
        self.tpa_extension: dict = None  # tpa_extension response

    def to_dict(self):
        return {
            "Status": self.status,
            "BrandFeatures": self.brand_feature,
            "PricedItineraries": self.priced_itinerarie,
            "TPA_Extensions": self.tpa_extension
        }
