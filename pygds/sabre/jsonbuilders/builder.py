

class SabreBFMBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, search_request, target: str = "Production", AvailableFlightsOnly: bool = True):
        self.target = target
        self.version = version
        self.AvailableFlightsOnly = True
        self.search_request = search_request

    def pos(self):
        return {
            "Source": [
                {
                    "RequestorID": {
                        "CompanyName": {
                            "Code": "TN",
                            "content": "Context"
                        },
                        "URL": "http://www.sabre.com/",
                        "Type": "1",
                        "ID": "1"
                    },
                    "PseudoCityCode": self.search_request["pcc"],
                    "ISOCountry": "US"
                }
            ]
        }

    def origin_destination_information(self):
        my_return = []
        itinaries = self.search_request["itineraries"}]
        for i in itinaries:
            my_return.append(
                {
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                        "CabinPref": {
                            "Cabin": self.search_request["csv"]
                        }
                    },
                    "RPH": str(itinaries.index(i) + 1),
                    "OriginLocation": {
                        "LocationCode": i["origin"],
                        "CodeContext": "IATA"
                    },
                    "DestinationLocation": {
                        "LocationCode": i["destination"],
                        "CodeContext": "IATA"
                    },
                    "DepartureDateTime": i["departureDate"] + "T11:00:00",
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                    }
                }
            )
        return my_return

    def trip_type(self):
        itin_count = len(self.search_request["itineraries"])
        if itin_count == 1:
            return "OneWay"
        
        if itin_count == 2:
            if self.search_request["itineraries"][0]["origin"] != self.search_request["itineraries"][1]["destination"] || self.search_request["itineraries"][0]["destination"] != self.search_request["itineraries"][1]["origin"]:
                return "OpenJaw"
            return "Return"
        
        if self.search_request["itineraries"][0]["origin"] == self.search_request["itineraries"][itin_count-1]["destination"]:
            return "Circle"

        return  "Other"


    def travel_preferences(self):
        cabin = self.search_request["csv"]
        paxTypeQuantityPUB = []
        paxTypeQuantityPFA = []
        
        if self.search_request["adult"]!=0:
            paxTypeQuantityPUB.append({
                "Code" : "ADT",
                "Quantity" : self.search_flight["adult"]

            })
            paxTypeQuantityPFA.append({
                "Code" : "PFA",
                "Quantity" : self.search_request["adult"]
            })

        if self.search_request["child"]!=0:
            paxTypeQuantityPUB.append({
                "Code" : "CNN",
                "Quantity" : self.search_flight["child"]

            })
            paxTypeQuantityPFA.append({
                "Code" : "CNN",
                "Quantity" : self.search_request["child"]
            })

        if self.search_request["infant"]!=0:
            paxTypeQuantityPUB.append({
                "Code" : "INF",
                "Quantity" : self.search_flight["infant"]

            })
            paxTypeQuantityPFA.append({
                "Code" : "INF",
                "Quantity" : self.search_request["infant"]
            })
        
        tpa_ext = {
            "LongConnectTime": {
                "Enable": true
            },
            "ExcludeVendorPref": [
                {
                    "Code": "WN"
                }
            ],
            "TripType": {
                "Value": self.trip_type()
            },
            "ExemptAllTaxes": {
                "Value": false
            },
            "ExemptAllTaxesAndFees": {
                "Value": false
            },
            "FlightStopsAsConnections": {
                "Ind": true
            },
            "JumpCabinLogic": {
                "Disabled": false
            },
            "DiversityParameters": {
                "Weightings": {
                    "PriceWeight": 10,
                    "TravelTimeWeight": 0
                },
                "AdditionalNonStopsPercentage": 100
            }
        }

        if  self.search_request["excludeBasicEconomy"] == true:
            tpa_ext = tpa_ext+","+"""FareType: [
                    {
                        "Code": "EOU",
                        "PreferLevel": "Unacceptable"
                    },
                    {
                        "Code": "ERU",
                        "PreferLevel": "Unacceptable"
                    }
                ]"""
        

    def travel_info_summary(self):
        pass  

    def  tpa_extensions(self):
        pass


    def itinaries(self):
        pass

    def search_flight(self):
        return {
            "OTA_AirLowFareSearchRQ": {
                "POS": self.pos(),
                "OriginDestinationInformation": self.origin_destination_information(),
                "TravelPreferences": self.travel_preferences(),
                "TravelerInfoSummary": self.travel_info_summary(),
                "TPA_Extensions": self.tpa_extensions(),
                "Target": "Production",
                "Version": "4.1.0",
                "AvailableFlightsOnly": true
            }

    def travel_preferences(self):
        pass

    def traveler_info_summary(self):
        pass

    def tpa_Extensions(self):
        pass
