"""from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from ..core import xmlparser
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json
import xmltodict
import json """


class FormatSoapSabre():
    # def __init__(self):
    #     pass
    def get_segment(segment_data):

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