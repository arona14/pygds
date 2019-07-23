from pygds.core.types import Passenger
from pygds.core.types import Itinerary, FlightPriceQuote, FlightSummary, FlightAmounts, FlightPassenger_pq, FlightSegment, FlightPointDetails, FormOfPayment, TicketingInfo, Remarks, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, PriceQuote
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

    # def get_segment(self, segment_data):
    #     '''
    #     This method returns all the segments of a given itineraries
    #     '''
    #     segment_datas = segment_data["stl18:Reservation"]["stl18:PassengerReservation"]["stl18:Segments"]["stl18:Segment"]
    #     segment_list = []
    #     if type(segment_datas) == list:
    #         for segment in segment_datas:
    #             if "stl18:Air" in segment:
    #                 s = {}
    #                 m = {}
    #                 s['Code'] = segment['stl18:Air']['Code']
    #                 s['ResBookDesigCode'] = segment['stl18:Air']['ResBookDesigCode']
    #                 s['StopQuantity'] = segment['stl18:Air']['StopQuantity']
    #                 s['DepartureAirport'] = segment['stl18:Air']['stl18:DepartureAirport']
    #                 s['DepartureAirportCodeContext'] = segment['stl18:Air']['stl18:DepartureAirportCodeContext']
    #                 s['DepartureTerminalName'] = segment['stl18:Air']['stl18:DepartureTerminalName']
    #                 s['DepartureTerminalCode'] = segment['stl18:Air']['stl18:DepartureTerminalCode']
    #                 s['ArrivalAirport'] = segment['stl18:Air']['stl18:ArrivalAirport']
    #                 s['ArrivalAirportCodeContext'] = segment['stl18:Air']['stl18:ArrivalAirportCodeContext']
    #                 if "stl18:ArrivalTerminalName" in segment['stl18:Air']:
    #                     s['ArrivalTerminalName'] = segment['stl18:Air']['stl18:ArrivalTerminalName']
    #                 else:
    #                     s['ArrivalTerminalName'] = ""
    #                 if "stl18:ArrivalTerminalCode" in segment['stl18:Air']:
    #                     s['ArrivalTerminalCode'] = segment['stl18:Air']['stl18:ArrivalTerminalCode']
    #                 else:
    #                     s['ArrivalTerminalCode'] = ""
    #                 s['OperatingAirlineCode'] = segment['stl18:Air']['stl18:OperatingAirlineCode']
    #                 s['OperatingAirlineShortName'] = segment['stl18:Air']['stl18:OperatingAirlineShortName']
    #                 s['OperatingFlightNumber'] = segment['stl18:Air']['stl18:OperatingFlightNumber']
    #                 s['EquipmentType'] = segment['stl18:Air']['stl18:EquipmentType']
    #                 s['MarketingAirlineCode'] = segment['stl18:Air']['stl18:MarketingAirlineCode']
    #                 s['MarketingFlightNumber'] = segment['stl18:Air']['stl18:MarketingFlightNumber']
    #                 s['OperatingClassOfService'] = segment['stl18:Air']['stl18:OperatingClassOfService']
    #                 s['OperatingClassOfService'] = segment['stl18:Air']['stl18:OperatingClassOfService']
    #                 s['MarketingClassOfService'] = segment['stl18:Air']['stl18:MarketingClassOfService']
    #                 m['Ind'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
    #                 m['Group'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
    #                 m['Sequence'] = segment['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
    #                 s['MarriageGrp'] = m
    #                 segment_list.append(s)
    #     else:
    #         if "stl18:Air" in segment_datas:
    #             s = {}
    #             m = {}
    #             s['Code'] = segment_datas['stl18:Air']['Code']
    #             s['ResBookDesigCode'] = segment_datas['stl18:Air']['ResBookDesigCode']
    #             s['StopQuantity'] = segment_datas['stl18:Air']['StopQuantity']
    #             s['DepartureAirport'] = segment_datas['stl18:Air']['stl18:DepartureAirport']
    #             s['DepartureAirportCodeContext'] = segment_datas['stl18:Air']['stl18:DepartureAirportCodeContext']
    #             s['DepartureTerminalName'] = segment_datas['stl18:Air']['stl18:DepartureTerminalName']
    #             s['DepartureTerminalCode'] = segment_datas['stl18:Air']['stl18:DepartureTerminalCode']
    #             s['ArrivalAirport'] = segment_datas['stl18:Air']['stl18:ArrivalAirport']
    #             s['ArrivalAirportCodeContext'] = segment_datas['stl18:Air']['stl18:ArrivalAirportCodeContext']
    #             if "stl18:ArrivalTerminalName" in segment_datas['stl18:Air']:
    #                 s['ArrivalTerminalName'] = segment_datas['stl18:Air']['stl18:ArrivalTerminalName']
    #             else:
    #                 s['ArrivalTerminalName'] = ""
    #             if "stl18:ArrivalTerminalCode" in segment_datas['stl18:Air']:
    #                 s['ArrivalTerminalCode'] = segment_datas['stl18:Air']['stl18:ArrivalTerminalCode']
    #             else:
    #                 s['ArrivalTerminalCode'] = ""
    #             s['OperatingAirlineCode'] = segment_datas['stl18:Air']['stl18:OperatingAirlineCode']
    #             s['OperatingAirlineShortName'] = segment_datas['stl18:Air']['stl18:OperatingAirlineShortName']
    #             s['OperatingFlightNumber'] = segment_datas['stl18:Air']['stl18:OperatingFlightNumber']
    #             s['EquipmentType'] = segment_datas['stl18:Air']['stl18:EquipmentType']
    #             s['MarketingAirlineCode'] = segment_datas['stl18:Air']['stl18:MarketingAirlineCode']
    #             s['MarketingFlightNumber'] = segment_datas['stl18:Air']['stl18:MarketingFlightNumber']
    #             s['OperatingClassOfService'] = segment_datas['stl18:Air']['stl18:OperatingClassOfService']
    #             s['OperatingClassOfService'] = segment_datas['stl18:Air']['stl18:OperatingClassOfService']
    #             s['MarketingClassOfService'] = segment_datas['stl18:Air']['stl18:MarketingClassOfService']
    #             m['Ind'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
    #             m['Group'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
    #             m['Sequence'] = segment_datas['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
    #             s['MarriageGrp'] = m
    #             segment_list.append(s)
    #     return segment_list

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
                res_book_desig_code = i['stl18:Air']['ResBookDesigCode']
                code_disclosure_carrier = i['stl18:Air']['stl18:DisclosureCarrier']['Code']
                dot = i['stl18:Air']['stl18:DisclosureCarrier']['DOT']
                banner = i['stl18:Air']['stl18:DisclosureCarrier']['stl18:Banner']
                ind = i['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
                group = i['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
                sequence = i['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
                content = ""
                depart_airport = i['stl18:Air']['stl18:DepartureAirport']
                arriv_airport = i['stl18:Air']['stl18:ArrivalAirport']
                operating_airline_code = i['stl18:Air']['stl18:OperatingAirlineCode']
                operating_short_name = i['stl18:Air']['stl18:OperatingAirlineShortName']
                if 'stl18:MarktingAirlineShortName' in i['stl18:Air']:
                    markting_short_name = i['stl18:Air']['stl18:MarktingAirlineShortName']
                else:
                    markting_short_name = ""
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
                markting_flight_number = i['stl18:Air']['stl18:MarketingFlightNumber']
                operating_flight_number = i['stl18:Air']['stl18:OperatingFlightNumber']
                class_of_service = i['stl18:Air']['stl18:ClassOfService']
                operating_class_of_service = i['stl18:Air']['stl18:OperatingClassOfService']
                markting_class_of_service = i['stl18:Air']['stl18:MarketingClassOfService']
                number_in_party = i['stl18:Air']['stl18:NumberInParty']
                out_bound_connection = i['stl18:Air']['stl18:outboundConnection']
                in_bound_connection = i['stl18:Air']['stl18:inboundConnection']
                airline_ref_id = str(i['stl18:Air']['stl18:AirlineRefId']).split('*')[1]
                if 'stl18:ElapsedTime' in i['stl18:Air']:
                    elapsed_time = i['stl18:Air']['stl18:ElapsedTime']
                else:
                    elapsed_time = ""
                seats = i['stl18:Air']['stl18:Seats']
                segment_special_requests = i['stl18:Air']['stl18:SegmentSpecialRequests']
                schedule_change_indicator = i['stl18:Air']['stl18:ScheduleChangeIndicator']
                segment_booked_date = i['stl18:Air']['stl18:SegmentBookedDate']
                air_miles_flown = i['stl18:Air']['stl18:AirMilesFlown']
                funnel_flight = i['stl18:Air']['stl18:FunnelFlight']
                change_of_gauge = i['stl18:Air']['stl18:ChangeOfGauge']
                # print(f"inbound: {in_bound_connection is True}, outbound: {out_bound_connection}")
                # itin = Itineraries(code, res_book_desig_code, departure_airport, arrival_airport, operating_airline_code, marketing_airline_code, equipment_type, eticket, departure_date_time, arrival_date_time, flight_number, class_of_service, number_in_party, out_bound_connection, in_bound_connection, airline_ref_id, elapsed_time)
                departure_airport = FlightPointDetails(content, depart_airport, departure_terminal_code)
                arrival_airport = FlightPointDetails(content, arriv_airport, arrival_terminal_code)
                marketing = FlightAirlineDetails(marketing_airline_code, markting_flight_number, markting_short_name, markting_class_of_service)
                operating = FlightAirlineDetails(operating_airline_code, operating_flight_number, operating_short_name, operating_class_of_service)
                disclosure_carrier = FlightDisclosureCarrier(code_disclosure_carrier, dot, banner)
                mariage_grp = FlightMarriageGrp(ind, group, sequence)
                index += 1
                segment = FlightSegment(index, res_book_desig_code, departure_date_time, departure_airport, arrival_date_time, arrival_airport, airline_ref_id, marketing, operating, disclosure_carrier, mariage_grp, seats, segment_special_requests, schedule_change_indicator, segment_booked_date, air_miles_flown, funnel_flight, change_of_gauge, flight_number, class_of_service, elapsed_time, equipment_type, eticket, number_in_party, code)
                if in_bound_connection == "false":  # begining of an itinerary
                    current_itinerary = Itinerary()
                    index = 0
                current_itinerary.addSegment(segment)
                if out_bound_connection == "false":  # end of an itinerary
                    result.append(current_itinerary)
        return result

    def price_quote(self, pricing_quote):
        price_data = []
        if pricing_quote is None:
            return price_data
        price_info = pricing_quote['PriceQuoteInfo']
        if not isinstance(price_info, list):
            price_info = [price_info]
        result = []
        for price in price_info:
            if 'Summary' in price:
                first_name = price['Summary']['NameAssociation']['firstName']
                last_name = price['Summary']['NameAssociation']['lastName']
                name_id = price['Summary']['NameAssociation']['nameId']
                name_number = price['Summary']['NameAssociation']['nameNumber']
                latest_pq_flag = price['Summary']['NameAssociation']['PriceQuote']['latestPQFlag']
                number = price['Summary']['NameAssociation']['PriceQuote']['number']
                pricing_type = price['Summary']['NameAssociation']['PriceQuote']['pricingType']
                status = price['Summary']['NameAssociation']['PriceQuote']['status']
                type_price_quote = price['Summary']['NameAssociation']['PriceQuote']['type']
                passenger_type_count = price['Summary']['NameAssociation']['PriceQuote']['Passenger']['passengerTypeCount']
                requested_type = price['Summary']['NameAssociation']['PriceQuote']['Passenger']['requestedType']
                type_passenger = price['Summary']['NameAssociation']['PriceQuote']['Passenger']['type']
                itinerary_type = price['Summary']['NameAssociation']['PriceQuote']['ItineraryType']
                validating_carrier = price['Summary']['NameAssociation']['PriceQuote']['ValidatingCarrier']
                currency_code = price['Summary']['NameAssociation']['PriceQuote']['Amounts']['Total']['currencyCode']
                decimal_place = price['Summary']['NameAssociation']['PriceQuote']['Amounts']['Total']['decimalPlace']
                text = price['Summary']['NameAssociation']['PriceQuote']['Amounts']['Total']['#text']
                local_create_date_time = price['Summary']['NameAssociation']['PriceQuote']['LocalCreateDateTime']
                passengers = FlightPassenger_pq(currency_code, decimal_place, text)
                pq = FlightPriceQuote(latest_pq_flag, number, pricing_type, status, type_price_quote, itinerary_type, validating_carrier, local_create_date_time)
                amounts = FlightAmounts(passenger_type_count, requested_type, type_passenger)
                summary = FlightSummary(first_name, last_name, name_id, name_number, pq, passengers, amounts)
                pricequote = PriceQuote(summary)
                result.append(pricequote)
        return result

        # details
        """
                number = 
                passenger_type = 
                pricing_type = 
                status = 
                type_details = 
                # AgentInfo
                duty = 
                sine = 
                home_location =
                work_location = 
                # TransactionInfo
                create_date_time = 
                update_date_time = 
                last_date_to_purchase = 
                local_creat_date_time = 
                input_entry = 
                # NameAssociationInfo
                first_name = 
                last_name = 
                name_id = 
                name_number = 
                # SegmentInfo
                number = 
                segment_status = 
                fare_basis = 
                not_valid_before =
                not_valid_after = 
                   # Baggage
                allowance = 
                type_bagage = 
                   # flight
                connection_indicator = 
                marketing_flight = 
                number = 
                text = 
                class_of_service =
                   #departure 
                date_time = 
                        # CityCode
                name = 
                    # arrival 
                date_time = 
                        # CityCode
                name = 
                text = 
            """

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
