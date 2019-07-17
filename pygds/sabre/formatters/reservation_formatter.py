from pygds.core.types import Passenger
from pygds.core.types import Itinerary, FlightSegment, FlightPointDetails, FormOfPayment, TicketingInfo, Remarks
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


class SabreReservationFormatter():
    def __init__(self):
        pass

    def get_segment(self, segment_data):
        '''
        This method returns all the segments of a given itineraries
        '''
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
        '''
        This method returns all the itineraries of a given sabre response
        itinerary = object_sabre['stl18:Reservation']['stl18:PassengerReservation']['stl18:Segments']
        '''
        origin_destination_option = []

        if itinerary is None:
            return origin_destination_option
        segments = itinerary['stl18:Segment']
        if not isinstance(segments, list):
            segments = [segments]
        print(f"length of segments: {len(segments)}")
        result = []  # list of itineraries
        current_itinerary = None
        index = 0
        for i in segments:
            if 'stl18:Air' in i:
                if 'Code' in i['stl18:Air']:
                    code = i['stl18:Air']['Code']
                else:
                    code = ""
                # res_book_desig_code = i['stl18:Air']['ResBookDesigCode']
                departure_airport = i['stl18:Air']['stl18:DepartureAirport']
                arrival_airport = i['stl18:Air']['stl18:ArrivalAirport']
                operating_airline_code = i['stl18:Air']['stl18:OperatingAirlineCode']
                marketing_airline_code = i['stl18:Air']['stl18:MarketingAirlineCode']
                equipment_type = i['stl18:Air']['stl18:EquipmentType']
                departure_terminal_code = i['stl18:Air']['stl18:DepartureTerminalCode']
                if 'stl18:ArrivalTerminalCode' in i['stl18:Air']:
                    arrival_terminal_code = i['stl18:Air']['stl18:ArrivalTerminalCode']
                else:
                    arrival_terminal_code = ""
                eticket = i['stl18:Air']['stl18:Eticket']
                departure_date_time = i['stl18:Air']['stl18:DepartureDateTime']
                arrival_date_time = i['stl18:Air']['stl18:ArrivalDateTime']
                flight_number = i['stl18:Air']['stl18:FlightNumber']
                class_of_service = i['stl18:Air']['stl18:ClassOfService']
                number_in_party = i['stl18:Air']['stl18:NumberInParty']
                out_bound_connection = i['stl18:Air']['stl18:outboundConnection']
                in_bound_connection = i['stl18:Air']['stl18:inboundConnection']
                airline_ref_id = str(i['stl18:Air']['stl18:AirlineRefId']).split('*')[1]
                if 'stl18:ElapsedTime' in i['stl18:Air']:
                    elapsed_time = i['stl18:Air']['stl18:ElapsedTime']
                else:
                    elapsed_time = ""
                time_zone = ""
                # print(f"inbound: {in_bound_connection is True}, outbound: {out_bound_connection}")
                # itin = Itineraries(code, res_book_desig_code, departure_airport, arrival_airport, operating_airline_code, marketing_airline_code, equipment_type, eticket, departure_date_time, arrival_date_time, flight_number, class_of_service, number_in_party, out_bound_connection, in_bound_connection, airline_ref_id, elapsed_time)
                departure = FlightPointDetails(departure_date_time, time_zone, "", "", departure_airport, "", departure_terminal_code)
                arrival = FlightPointDetails(arrival_date_time, time_zone, "", "", arrival_airport, "", arrival_terminal_code)
                index += 1
                segment = FlightSegment(index, departure, arrival, airline_ref_id, marketing_airline_code, operating_airline_code, flight_number, class_of_service, elapsed_time, equipment_type, eticket, number_in_party, code)
                if in_bound_connection == "false":  # begining of an itinerary
                    current_itinerary = Itinerary()
                    index = 0
                current_itinerary.addSegment(segment)
                if out_bound_connection == "false":  # end of an itinerary
                    result.append(current_itinerary)
        return result

    def formofpayment(self, forms_of_payment):
        formof_payment_list = []
        if forms_of_payment is None:
            return formof_payment_list
        short_text = forms_of_payment['stl18:FormsOfPayment']
        if not isinstance(short_text, list):
            short_text = [short_text]
        result = []
        for i in short_text:
            if 'stl18:CreditCardPayment' in i:
                if 'ShortText' in i['stl18:CreditCardPayment']:
                    sh_text = i['stl18:CreditCardPayment']['ShortText']
                else:
                    sh_text = ""
            objet = FormOfPayment(sh_text)
            result.append(objet)
        return result

    def ticketing_info(self, ticket):
        list_ticket = []
        if ticket is None:
            return list_ticket
        ticket_info = ticket['stl18:TicketingInfo']
        if not isinstance(ticket_info, list):
            ticket_info = [ticket_info]
        result = []
        for tick in ticket_info:
            if 'stl18:FutureTicketing' in tick:
                id_ticket = tick['stl18:FutureTicketing']['id']
                index = tick['stl18:FutureTicketing']['index']
                element_id = tick['stl18:FutureTicketing']['elementId']
                code = tick['stl18:FutureTicketing']['stl18:Code']
                branch_pcc = tick['stl18:FutureTicketing']['stl18:BranchPCC']
                date = tick['stl18:FutureTicketing']['stl18:Date']
                time = tick['stl18:FutureTicketing']['stl18:Time']
                queue_number = tick['stl18:FutureTicketing']['stl18:QueueNumber']
                comment = tick['stl18:FutureTicketing']['stl18:Comment']
                ticketinf = TicketingInfo(id_ticket, index, element_id, code, branch_pcc, date, time, queue_number, comment)
                result.append(ticketinf)
        return result

    def get_remarks(self, remarks_data):
        remark_list = []
        if remarks_data is None:
            return remark_list
        remarks = remarks_data['stl18:Remarks']['stl18:Remark']
        if not isinstance(remarks, list):
            remarks = [remarks]
        # print(f"length of remarks: {len(remarks)}")
        result = []
        index = 0
        for remark in remarks:
            if 'type' in remark:
                type_rem = remark['type']
            else:
                type_rem = ""
            if 'elementId' in remark:
                element_id = remark['elementId']
            else:
                element_id = ""
            text = remark['stl18:RemarkLines']['stl18:RemarkLine']['stl18:Text']
            index += 1
            remark_objet = Remarks(index, type_rem, element_id, text)
            result.append(remark_objet)
        return result

    def get_passengers(self, data):
        passengers_data = data["stl18:Reservation"]["stl18:PassengerReservation"]["stl18:Passengers"]
        passenger_list = []
        if type(passengers_data) == list:
            for passengers in passengers_data:
                if "stl18:Passenger" in passengers:
                    name_id = passengers_data['stl18:Passenger']['nameId']
                    pax_type = passengers_data['stl18:Passenger']['passengerType']
                    last_name = passengers_data['stl18:Passenger']['stl18:LastName']
                    first_name = passengers_data['stl18:Passenger']['stl18:FirstName']
                    date_of_birth = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:DateOfBirth']
                    gender = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Gender']
                    surname = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Surname']
                    forename = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Forename']
                    middle_name = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:MiddleName']
                    action_code = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:ActionCode']
                    number_in_party = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:NumberInParty']
                    vendor_code = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:VendorCode']
                    p = Passenger(name_id, first_name, last_name, date_of_birth, gender, surname, forename, middle_name, action_code, number_in_party, vendor_code, pax_type)
                    passenger_list.append(p)
        else:
            if "stl18:Passenger" in passengers_data:
                name_id = passengers_data['stl18:Passenger']['nameId']
                pax_type = passengers_data['stl18:Passenger']['passengerType']
                last_name = passengers_data['stl18:Passenger']['stl18:LastName']
                first_name = passengers_data['stl18:Passenger']['stl18:FirstName']
                date_ofBirth = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:DateOfBirth']
                gender = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Gender']
                surname = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Surname']
                forename = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:Forename']
                middle_name = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:MiddleName']
                action_code = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:ActionCode']
                number_in_party = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:NumberInParty']
                vendor_code = passengers_data['stl18:Passenger']['stl18:SpecialRequests']['stl18:APISRequest']['stl18:DOCSEntry']['stl18:VendorCode']
                p = Passenger(name_id, first_name, last_name, date_ofBirth, gender, surname, forename, middle_name, action_code, number_in_party, vendor_code, pax_type)
                passenger_list.append(p)
        return passenger_list
