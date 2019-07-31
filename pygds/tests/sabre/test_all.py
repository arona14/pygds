"""
    This is for testing purposes like a suite.
"""
import os
import jxmlease
import  json
import requests

from pygds.core.helpers import get_data_from_xml
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds import log_handler
from pygds.sabre.client import SabreClient
from pygds.core.request import LowFareSearchRequest




final_object = """{
    "OTA_AirLowFareSearchRQ": {
        {"POS": {"Source": [{"RequestorID":
         {"CompanyName": {"Code": "TN", "content": "Context"}, 
         "URL": "http://www.sabre.com/", "Type": "1", "ID": "1"},
          "PseudoCityCode": "WR17", "ISOCountry": "US"}]},
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
#final_object_json = json.loads(final_object)

def test():
    """ A suite of tests """

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #log = log_handler.get_logger("test_all")
    #pnr = "RH3WOD"  # "Q68EFX", "RI3B6D", "RT67BC"
    # m_id = None
    
    urlpattern = "https://api.havail.sabre.com" + "/v4.1.0/shop/flights?mode=live"

    client = SabreClient(url, username, password, pcc, False)
    #try:
    session_response = client.session_token()
    #token = jxmlease.parse(session_response)
    #token = token[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']
    #token = "T1RLAQK+khi8F8dRN8jb/0I3vycaNfNsVhCi3oz+LENCh5rPk0AP35wAAACwH2I1Tqcjy5St6cR9b2jzIjOr8ESwaZU3JYCfRp0kBft9dKT3TU5vi3aUV6mXVo1ARc+JU2hMIV7iYfbd17dTWnTQ3YwssvtO831ba+frT1ilCOHhyloEmUJxspZIaLx5hza8mrKVxdBXj60C4T7NBiBGNFZm4B0dtbZP3cWrdEltU9Oz3mExWxmlkQYxmlCrlB0/KbWMDl4a4IuxFyBM2eEd49d4Dw2HJVhAx1GE1eM*"
    my_request = LowFareSearchRequest([{"origin": "DTW","destination": "CDG","departureDate": "2019-10-23"}, 
                { "origin": "CDG", "destination": "NYC","departureDate": "2019-11-22"}],"Y","WR17",1,0,0,[],"",[],False,True)
    token_return  = get_data_from_xml(session_response,"soap-env:Envelope",'soap-env:Header',"wsse:Security","wsse:BinarySecurityToken")["#text"]
    print(type(my_request))
    
    
        #log.info(session_response)
    #except ClientError as ce:
        #log.error(f"client_error: {ce}")
        #log.error(f"session: {ce.session_info}")
    #except ServerError as se:
        #log.error(f"server_error: {se}")
        #log.error(f"session: {se.session_info}")
    """ 
        Test Search Flight Sabre 
    """
    search_data = client.search_flightrq(my_request)
    search_data = json.dumps(search_data)
    print(search_data)
    #print(search_data)
    header = {
            'Authorization' : "Bearer " + token_return,
            'Content-Type': 'application/json; charset=utf-8'
        }
    response = requests.post(urlpattern, data=search_data, headers=header)
    response = json.loads(response.content)
    return response

if __name__ == "__main__":
    result = test()
    result = json.dumps(dict(result), sort_keys=False, indent=4)
    with open("myResult.json", 'w') as myFile:
        myFile.write(str(result))
    myFile.close()
