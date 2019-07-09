"""from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from ..core import xmlparser
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json
import xmltodict
import json """
'''from datetime import datetime, timedelta, date
from decimal import Decimal
import json, operator '''


class FormatSoapSabre():
    # def __init__(self):
    #     pass
    def get_segment(self, segment_data):

        segment_datas = segment_data["stl18:Reservation"]["stl18:PassengerReservation"]["stl18:Segments"]["stl18:Segment"]
        segment_list = []
        if type(segment_datas) == list:
            for segment in segment_datas:
                if "stl18:Air" in segment:
                    s = {}
                    m = {}
                    s['Code'] = segment['stl18:Air']['Code']
                    s['ResBookDesigCode'] = segment['stl18:Air']['ResBookDesigCode']
                    s['StopQuantity'] = segment['stl18:Air']['StopQuantity']
                    s['DepartureAirport'] = segment['stl18:Air']['stl18:DepartureAirport']
                    s['DepartureAirportCodeContext'] = segment['stl18:Air']['stl18:DepartureAirportCodeContext']
                    s['DepartureTerminalName'] = segment['stl18:Air']['stl18:DepartureTerminalName']
                    s['DepartureTerminalCode'] = segment['stl18:Air']['stl18:DepartureTerminalCode']
                    s['ArrivalAirport'] = segment['stl18:Air']['stl18:ArrivalAirport']
                    s['ArrivalAirportCodeContext'] = segment['stl18:Air']['stl18:ArrivalAirportCodeContext']
                    if "stl18:ArrivalTerminalName" in segment['stl18:Air']:
                        s['ArrivalTerminalName'] = segment['stl18:Air']['stl18:ArrivalTerminalName']
                    else:
                        s['ArrivalTerminalName'] = ""
                    if "stl18:ArrivalTerminalCode" in segment['stl18:Air']:
                        s['ArrivalTerminalCode'] = segment['stl18:Air']['stl18:ArrivalTerminalCode']
                    else:
                        s['ArrivalTerminalCode'] = ""
                    s['OperatingAirlineCode'] = segment['stl18:Air']['stl18:OperatingAirlineCode']
                    s['OperatingAirlineShortName'] = segment['stl18:Air']['stl18:OperatingAirlineShortName']
                    s['OperatingFlightNumber'] = segment['stl18:Air']['stl18:OperatingFlightNumber']
                    s['EquipmentType'] = segment['stl18:Air']['stl18:EquipmentType']
                    s['MarketingAirlineCode'] = segment['stl18:Air']['stl18:MarketingAirlineCode']
                    s['MarketingFlightNumber'] = segment['stl18:Air']['stl18:MarketingFlightNumber']
                    s['OperatingClassOfService'] = segment['stl18:Air']['stl18:OperatingClassOfService']
                    s['OperatingClassOfService'] = segment['stl18:Air']['stl18:OperatingClassOfService']
                    s['MarketingClassOfService'] = segment['stl18:Air']['stl18:MarketingClassOfService']
                    m['Ind'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
                    m['Group'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
                    m['Sequence'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
                    s['MarriageGrp'] = m
                    segment_list.append(s)
        else:
            if "stl18:Air" in segment_datas:
                s = {}
                m = {}
                s['Code'] = segment_datas['stl18:Air']['Code']
                s['ResBookDesigCode'] = segment_datas['stl18:Air']['ResBookDesigCode']
                s['StopQuantity'] = segment_datas['stl18:Air']['StopQuantity']
                s['DepartureAirport'] = segment_datas['stl18:Air']['stl18:DepartureAirport']
                s['DepartureAirportCodeContext'] = segment_datas['stl18:Air']['stl18:DepartureAirportCodeContext']
                s['DepartureTerminalName'] = segment_datas['stl18:Air']['stl18:DepartureTerminalName']
                s['DepartureTerminalCode'] = segment_datas['stl18:Air']['stl18:DepartureTerminalCode']
                s['ArrivalAirport'] = segment_datas['stl18:Air']['stl18:ArrivalAirport']
                s['ArrivalAirportCodeContext'] = segment_datas['stl18:Air']['stl18:ArrivalAirportCodeContext']
                if "stl18:ArrivalTerminalName" in segment_datas['stl18:Air']:
                    s['ArrivalTerminalName'] = segment_datas['stl18:Air']['stl18:ArrivalTerminalName']
                else:
                    s['ArrivalTerminalName'] = ""
                if "stl18:ArrivalTerminalCode" in segment_datas['stl18:Air']:
                    s['ArrivalTerminalCode'] = segment_datas['stl18:Air']['stl18:ArrivalTerminalCode']
                else:
                    s['ArrivalTerminalCode'] = ""
                s['OperatingAirlineCode'] = segment_datas['stl18:Air']['stl18:OperatingAirlineCode']
                s['OperatingAirlineShortName'] = segment_datas['stl18:Air']['stl18:OperatingAirlineShortName']
                s['OperatingFlightNumber'] = segment_datas['stl18:Air']['stl18:OperatingFlightNumber']
                s['EquipmentType'] = segment_datas['stl18:Air']['stl18:EquipmentType']
                s['MarketingAirlineCode'] = segment_datas['stl18:Air']['stl18:MarketingAirlineCode']
                s['MarketingFlightNumber'] = segment_datas['stl18:Air']['stl18:MarketingFlightNumber']
                s['OperatingClassOfService'] = segment_datas['stl18:Air']['stl18:OperatingClassOfService']
                s['OperatingClassOfService'] = segment_datas['stl18:Air']['stl18:OperatingClassOfService']
                s['MarketingClassOfService'] = segment_datas['stl18:Air']['stl18:MarketingClassOfService']
                m['Ind'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
                m['Group'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
                m['Sequence'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
                s['MarriageGrp'] = m
                segment_list.append(s)
        return segment_list

    def days(self, weekday):
        if weekday == 0:
            return 'Mon'
        if weekday == 1:
            return 'Tue'
        if weekday == 2:
            return 'Wed'
        if weekday == 3:
            return 'Thu'
        if weekday == 4:
            return 'Fri'
        if weekday == 5:
            return 'Sat'
        if weekday == 6:
            return 'Sun'
    
    def itineraryInfo(self, itinerary):
        origin_destination_option = []
        flight_segment = []
        if itinerary is None:
            return origin_destination_option
        segments = itinerary['stl18:Segment']
        if type(segments) == list:
            for i in segments:
                if 'stl18:Air' in i:
                    segment_data = {}
                    if 'Code' in i['stl18:Air']:
                        segment_data['Code'] = i['stl18:Air']['Code']
                    else:
                        segment_data['Code'] = ""                        
                    segment_data['ResBookDesigCode'] = i['stl18:Air']['ResBookDesigCode']                   
                    segment_data['DepartureAirport'] = i['stl18:Air']['stl18:DepartureAirport']
                    segment_data['ArrivalAirport'] = i['stl18:Air']['stl18:ArrivalAirport']
                    segment_data['OperatingAirlineCode'] = i['stl18:Air']['stl18:OperatingAirlineCode']
                    segment_data['MarketingAirlineCode'] = i['stl18:Air']['stl18:MarketingAirlineCode']
                    segment_data['EquipmentType'] = i['stl18:Air']['stl18:EquipmentType']
                    segment_data['Eticket'] = i['stl18:Air']['stl18:Eticket']
                    segment_data['DepartureDateTime'] = i['stl18:Air']['stl18:DepartureDateTime']
                    segment_data['ArrivalDateTime'] = i['stl18:Air']['stl18:ArrivalDateTime']
                    segment_data['FlightNumber'] = i['stl18:Air']['stl18:FlightNumber']
                    segment_data['ClassOfService'] = i['stl18:Air']['stl18:ClassOfService']
                    segment_data['NumberInParty'] = i['stl18:Air']['stl18:NumberInParty']
                    segment_data['OutboundConnection'] = i['stl18:Air']['stl18:outboundConnection']
                    segment_data['InboundConnection'] = i['stl18:Air']['stl18:inboundConnection']
                    segment_data['AirlineRefId'] = str(i['stl18:Air']['stl18:AirlineRefId']).split('*')[1] 

                    if 'stl18:ElapsedTime' in i['stl18:Air']:
                        segment_data['ElapsedTime'] = i['stl18:Air']['stl18:ElapsedTime']
                    else:
                        segment_data['ElapsedTime'] = "" 
                    flight_segment.append(segment_data)
                    if segment_data['OutboundConnection'] == "false":
                        origin_destination_option.append({"FlightSegment": flight_segment})
                        flight_segment = []
        else:
            if 'stl18:Air' in segments:
                segment_data = {}
                if 'Code' in segments['stl18:Air']:
                    segment_data['Code'] = segments['stl18:Air']['Code']
                else:
                    segment_data['Code'] = ""                        
                segment_data['ResBookDesigCode'] = segments['stl18:Air']['ResBookDesigCode']                   
                segment_data['DepartureAirport'] = segments['stl18:Air']['stl18:DepartureAirport']
                segment_data['ArrivalAirport'] = segments['stl18:Air']['stl18:ArrivalAirport']
                segment_data['OperatingAirlineCode'] = segments['stl18:Air']['stl18:OperatingAirlineCode']
                segment_data['MarketingAirlineCode'] = segments['stl18:Air']['stl18:MarketingAirlineCode']
                segment_data['EquipmentType'] = segments['stl18:Air']['stl18:EquipmentType']
                segment_data['Eticket'] = segments['stl18:Air']['stl18:Eticket']
                segment_data['DepartureDateTime'] = segments['stl18:Air']['stl18:DepartureDateTime']
                segment_data['ArrivalDateTime'] = segments['stl18:Air']['stl18:ArrivalDateTime']
                segment_data['FlightNumber'] = segments['stl18:Air']['stl18:FlightNumber']
                segment_data['ClassOfService'] = segments['stl18:Air']['stl18:ClassOfService']
                segment_data['NumberInParty'] = segments['stl18:Air']['stl18:NumberInParty']
                segment_data['OutboundConnection'] = segments['stl18:Air']['stl18:outboundConnection']
                segment_data['InboundConnection'] = segments['stl18:Air']['stl18:inboundConnection']
                segment_data['AirlineRefId'] = str(segments['stl18:Air']['stl18:AirlineRefId']).split('*')[1] 

                if 'stl18:ElapsedTime' in segments['stl18:Air']:
                    segment_data['ElapsedTime'] = segments['stl18:Air']['stl18:ElapsedTime']
                else:
                    segment_data['ElapsedTime'] = "" 

                flight_segment.append(segment_data)
                
                origin_destination_option.append({"FlightSegment": flight_segment})
                
        return origin_destination_option
                
    def get_passengers(data):
        passengers_data = data["stl18:Reservation"]["stl18:PassengerReservation"]["stl18:Passengers"]
        passenger_list = []
        if type(passengers_data) == list:
            for passengers in passengers_data:
                if "stl18:Passenger" in passengers:
                    p = {}
                    p_to = {}
                    p['NameAssocId'] = passengers['stl18:Passenger']['nameAssocId']
                    p['LastName'] = passengers['stl18:Passenger']['stl18:LastName']
                    p['FirstName'] = passengers['stl18:Passenger']['stl18:FirstName']
                    p_to['DateOfBirth'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:DateOfBirth']
                    p_to['Gender'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Gender']
                    p_to['Surname'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Surname']
                    p_to['Forename'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Forename']
                    p_to['MiddleName'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:MiddleName']
                    p_to['ActionCode'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:ActionCode']
                    p_to['NumberInParty'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:NumberInParty']
                    p_to['VendorCode'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:VendorCode']
                    p['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry'] = p_to
                    passenger_list.append(p)
        else:
            if "stl18:Passenger" in passengers:
                p = {}
                p_to = {}
                p['NameAssocId'] = passengers['stl18:Passenger']['nameAssocId']
                p['LastName'] = passengers['stl18:Passenger']['stl18:LastName']
                p['FirstName'] = passengers['stl18:Passenger']['stl18:FirstName']
                p_to['DateOfBirth'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:DateOfBirth']
                p_to['Gender'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Gender']
                p_to['Surname'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Surname']
                p_to['Forename'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Forename']
                p_to['MiddleName'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:MiddleName']
                p_to['ActionCode'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:ActionCode']
                p_to['NumberInParty'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:NumberInParty']
                p_to['VendorCode'] = passengers['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:VendorCode']
                p['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry'] = p_to
                passenger_list.append(p)
        return passenger_list