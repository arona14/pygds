import requests
from .helpers import soap_service_to_json
from .session import SabreSession
from pygds import env_settings
from pygds.sabre.config import sabre_credentials, decode_base64
import json


my_json = """{
    "OTA_AirLowFareSearchRQ": {
        "POS": {
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
                    "PseudoCityCode": "WR17",
                    "ISOCountry": "US"
                }
            ]
        },
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
                "NegotiatedFaresOnly": false
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

urlpattern = "https://api.havail.sabre.com" + "/v1/offers/shop"


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
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip,deflate',
        }
        response = requests.post(urlpattern, data=datas, headers=header)
        response = json.loads(response.content)
        return response


if __name__ == "__main__":
    result = My_test().post(my_json)
    result = str(result)
    with open("myResult.json", 'w') as myFile:
        myFile.write(result)
