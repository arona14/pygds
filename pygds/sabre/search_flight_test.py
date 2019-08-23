import requests
import json
from .session import SabreSession
from pygds import env_settings
from pygds.sabre.config import decode_base64


request = """{"itineraries": [{"origin": "RDU","destination": "HYD","departureDate":"2019-10-23"},
                { "origin": "BLR", "destination": "RDU","departureDate": "2019-11-22"}], "csv": "Y", "pcc": "WR17", "adult": 1,"child":0,
                "infant": 0,"alternatePcc": [],"requestType": "200ITINS", "preferredAirlines": ["GF"],
                "baggagePref": false,"excludeBasicEconomy": true }"""

request_json = json.loads(request)
# print(request_json)

final_object = """{
    "OTA_AirLowFareSearchRQ": {
        "POS" : "SabreBFMBuilder().pos()",
        "OriginDestinationInformation": [
            {
                "TPA_Extensions": {
                    "SegmentType": {
                        "Code": "O"
                    },
                    "CabinPref": {
                        "Cabin": "Y"
                    }
                },
                "RPH": "1",
                "OriginLocation": {
                    "LocationCode": "DTW",
                    "CodeContext": "IATA"
                },
                "DestinationLocation": {
                    "LocationCode": "CDG",
                    "CodeContext": "IATA"
                },
                "DepartureDateTime": "2019-10-08T11:00:00"
            },
            {
                "TPA_Extensions": {
                    "SegmentType": {
                        "Code": "O"
                    },
                    "CabinPref": {
                        "Cabin": "Y"
                    }
                },
                "RPH": "2",
                "OriginLocation": {
                    "LocationCode": "CDG",
                    "CodeContext": "IATA"
                },
                "DestinationLocation": {
                    "LocationCode": "DTW",
                    "CodeContext": "IATA"
                },
                "DepartureDateTime": "2019-10-21T11:00:00"
            }
        ],
        "TravelPreferences": {
            "ValidInterlineTicket": true,
            "FlightTypePref": {
                "MaxConnections": "2"
            },
            "TPA_Extensions": {
                "LongConnectTime": {
                    "Enable": true
                },
                "ExcludeVendorPref": [
                    {
                        "Code": "WN"
                    }
                ],
                "TripType": {
                    "Value": "Return"
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
                "FlexibleFares": {
                    "FareParameters": [
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "JCB",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "JNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "JNF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "Y"
                            },
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        },
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "ADT",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "CNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "INF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "Y"
                            },
                            "NegotiatedFaresOnly": {
                                "Ind": true
                            },
                            "AccountCode": [
                                {
                                    "Code": "COM"
                                }
                            ],
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        },
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "PFA",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "CNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "INF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "Y"
                            },
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        },
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "JCB",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "JNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "JNF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "S"
                            },
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        },
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "ADT",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "CNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "INF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "S"
                            },
                            "NegotiatedFaresOnly": {
                                "Ind": true
                            },
                            "AccountCode": [
                                {
                                    "Code": "COM"
                                }
                            ],
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        },
                        {
                            "PassengerTypeQuantity": [
                                {
                                    "Code": "PFA",
                                    "Quantity": 2
                                },
                                {
                                    "Code": "CNN",
                                    "Quantity": 1
                                },
                                {
                                    "Code": "INF",
                                    "Quantity": 1
                                }
                            ],
                            "Cabin": {
                                "Type": "S"
                            },
                            "VoluntaryChanges": {
                                "Match": "Info",
                                "Penalty": [
                                    {
                                        "Type": "Refund"
                                    },
                                    {
                                        "Type": "Exchange"
                                    }
                                ]
                            }
                        }
                    ]
                },
                "DiversityParameters": {
                    "Weightings": {
                        "PriceWeight": 10,
                        "TravelTimeWeight": 0
                    },
                    "AdditionalNonStopsPercentage": 100
                }
            },
            "AncillaryFees": {
                "Enable": true,
                "Summary": true,
                "AncillaryFeeGroup": [
                    {
                        "Code": "BG",
                        "Count": "3"
                    }
                ]
            }
        },
        "TravelerInfoSummary": {
            "AirTravelerAvail": [
                {
                    "PassengerTypeQuantity": [
                        {
                            "Code": "JCB",
                            "Quantity": 2,
                            "TPA_Extensions": {
                                "VoluntaryChanges": {
                                    "Match": "Info",
                                    "Penalty": [
                                        {
                                            "Type": "Refund"
                                        },
                                        {
                                            "Type": "Exchange"
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "Code": "CNN",
                            "Quantity": 1,
                            "TPA_Extensions": {
                                "VoluntaryChanges": {
                                    "Match": "Info",
                                    "Penalty": [
                                        {
                                            "Type": "Refund"
                                        },
                                        {
                                            "Type": "Exchange"
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "Code": "INF",
                            "Quantity": 1,
                            "TPA_Extensions": {
                                "VoluntaryChanges": {
                                    "Match": "Info",
                                    "Penalty": [
                                        {
                                            "Type": "Refund"
                                        },
                                        {
                                            "Type": "Exchange"
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            ],
            "PriceRequestInformation": {
                "NegotiatedFareCode": [],
                "TPA_Extensions": {
                    "Priority": {
                        "Price": {
                            "Priority": 1
                        },
                        "DirectFlights": {
                            "Priority": 4
                        },
                        "Time": {
                            "Priority": 2
                        },
                        "Vendor": {
                            "Priority": 3
                        }
                    },
                    "Indicators": {
                        "RefundPenalty": {
                            "Ind": true
                        }
                    },
                    "BrandedFareIndicators": {
                        "SingleBrandedFare": true,
                        "MultipleBrandedFares": false
                    }
                },
                "NegotiatedFaresOnly": "false"
            }
        },
        "TPA_Extensions": {
            "IntelliSellTransaction": {
                "RequestType": {
                    "Name": "50ITINS"
                },
                "CompressResponse": {
                    "Value": true
                }
            },
            "MultiTicket": {
                "DisplayPolicy": "SOW"
            },
            "AlternatePCC": []
        },
        "Target": "Production",
        "Version": "4.1.0",
        "AvailableFlightsOnly": true
    }
}
"""
final_object_json = json.loads(final_object)

# print(final_object_json)

urlpattern = "https://api.havail.sabre.com" + "/v4.3.0/shop/flights?mode=live"


class My_test:

    def post(self, datas):
        url = "https://webservices3.sabre.com"
        headers = {'content-type': 'text/xml'}
        conversation_id = "cosmo-material-02cc7cd0-90ef-11e9-b8ee-bba9bb4fc857"
        username = env_settings.get_setting("SABRE_USERNAME")
        pcc = env_settings.get_setting("SABRE_PCC")
        password = decode_base64(env_settings.get_setting("SABRE_PASSWPRD"))

        token = SabreSession(pcc, username, password, conversation_id, url, headers).open()
        print(token)

        header = {
            'Authorization': "Bearer " + token,
            'Content-Type': 'application/json'
        }
        response = requests.post(urlpattern, data=datas, headers=header)
        response = json.loads(response.text)
        return response


"""
result = My_test().post(my_json)
result = str(result)
with open("myResult.text", 'w') as myFile:
myFile.write(result)
myFile.close()
"""
if __name__ == "__main__":
    # datas = SearchFlightRequest(request_json)
    # print(datas)
    # print(SabreBFMBuilder(datas).search_flight())
    pass
