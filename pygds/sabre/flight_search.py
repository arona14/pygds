from pygds.core.types import BasicDataObject
import json 
from typing import  List



class Itinaries(BasicDataObject):

    def  __init__(self, origin: str = None, destination: str = None, departureDate: str = None):
        self.origin = origin
        self.destination = destination
        self.departureDate = departureDate

    def to_data(self):
        return  {
            "origin" : self.origin,
            "destination" : self.destination,
            "departureDate" : self.departureDate
        }


class SearchFlightRequest(BasicDataObject):
    """
        This  class will return  a json to search flight
    """

    def  __init__(self,itineraries: Itinaries = [], pcc: str = None, adult: int = 0, child:int = 0, infant: int = 0, csv: str = None, alternatePcc: list = [], requestType: str = None, preferredAirlines: list = [], baggagePref: bool = False, excludeBasicEconomy: bool = True ):
        self.itineraries: List[Itinaries] = itineraries
        self.pcc = pcc 
        self.adult = adult
        self.child = child  
        self.infant = infant
        self.csv = csv  
        self.alternatePcc = alternatePcc
        self.requestType = requestType
        self.preferredAirlines = preferredAirlines
        self.baggagePref = baggagePref
        self.excludeBasicEconomy = excludeBasicEconomy


    def to_data(self):
        return {
            "itineraries": [i for i in self.itineraries],
            "pcc": self.pcc,
            "adult": self.adult,
            "child" : self.child,
            "infant" : self.infant,
            "csv": self.csv,
            "alternatePcc": [al for al in self.alternatePcc],
            "requestType" : self.requestType,
            "preferredAirlines" : self.preferredAirlines,
            "baggagePref" : self.baggagePref,
            "excludeBasicEconomy" : self.excludeBasicEconomy

        }







if __name__ == "__main__":
    test = SearchFlightRequest([{"origin": "RDU","destination": "HYD","departureDate": "2019-10-23"},{"origin": "BLR", "destination": "RDU", "departureDate": "2019-11-22" }]).to_data()["itineraries"]
    print(test)