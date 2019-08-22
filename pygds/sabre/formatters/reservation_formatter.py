from pygds.core.app_error import ApplicationError
from pygds.core.sessions import SessionInfo
from pygds.core.types import Passenger
from pygds.core.types import Itinerary, FlightPriceQuote, FlightSummary, FlightAmounts, FlightPassenger_pq, FlightSegment, FlightPointDetails, FormOfPayment, TicketingInfo, Remarks, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, PriceQuote,TicketingInfo_
from pygds.sabre.helpers import get_data_from_json as from_json
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list,get_data_from_xml as from_xml, reformat_date,ensureList



class BaseResponseExtractor:
    """
    This class is for holding a parsed response from GDS. It will include the session information and the useful data (payload)
    """

    def __init__(self, session_info: SessionInfo, payload=None, app_error: ApplicationError = None):
        self.session_info = session_info
        self.payload = payload
        self.application_error = app_error

    def to_dict(self):
        return {
            "session_info": None if not self.session_info else self.session_info.__str__(),
            "payload": str(self.payload),
            "application_error": self.application_error.to_dict() if self.application_error else None
        }

    def __str__(self):
        return str(self.to_dict())

class SabreReservationFormatter():
    
    def __init__(self, xml_content: str):
        self.xml_content = xml_content
    
    def _extract(self):

        display_pnr = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body","stl18:GetReservationRS")
        display_pnr = str(display_pnr).replace("@","")
        display_pnr = eval(display_pnr.replace("u'","'"))
        return {
            'passengers': self._passengers(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:Passengers']['stl18:Passenger']),
            'itineraries': self._itineraries(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:Segments']),
            'form_of_payments': self._forms_of_payment(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:FormsOfPayment']),
            'price_quotes': None,
            'ticketing_info': self._ticketing(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:TicketingInfo']),
            'remarks': self._remarks(display_pnr['stl18:Reservation']['stl18:Remarks']["stl18:Remark"]),
            'dk_number': display_pnr['stl18:Reservation']['stl18:DKNumbers']["stl18:DKNumber"]
        }

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

    def _itineraries(self, itinerary):

        if itinerary is None:
            return []
        list_itineraries = []  # list of itineraries
        current_itinerary = None
        index = 0
        for i in ensureList(itinerary['stl18:Segment']):
            if 'stl18:Air' in i:
                if 'Code' in i['stl18:Air']:
                    code = i['stl18:Air']['Code']
                else:
                    code = ""
                res_book_desig_code = i['stl18:Air']['ResBookDesigCode']
                code_disclosure_carrier = ""
                dot = ""
                banner = ""
                ind = i['stl18:Air']['stl18:MarriageGrp']['stl18:Ind']
                group = i['stl18:Air']['stl18:MarriageGrp']['stl18:Group']
                sequence = i['stl18:Air']['stl18:MarriageGrp']['stl18:Sequence']
                depart_airport = i['stl18:Air']['stl18:DepartureAirport']
                arrival_airport = i['stl18:Air']['stl18:ArrivalAirport']
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
                action_code = i['stl18:Air']['stl18:ActionCode']
                departure_airport = FlightPointDetails(departure_date_time, depart_airport, departure_terminal_code)
                arrival_airport = FlightPointDetails(arrival_date_time, arrival_airport, arrival_terminal_code)
                marketing = FlightAirlineDetails(marketing_airline_code, markting_flight_number, markting_short_name, markting_class_of_service)
                operating = FlightAirlineDetails(operating_airline_code, operating_flight_number, operating_short_name, operating_class_of_service)
                disclosure_carrier = FlightDisclosureCarrier(code_disclosure_carrier, dot, banner)
                mariage_grp = FlightMarriageGrp(ind, group, sequence)
                index += 1
                segment = FlightSegment(index, res_book_desig_code, departure_date_time, departure_airport, arrival_date_time, arrival_airport, airline_ref_id, marketing, operating, disclosure_carrier, mariage_grp, seats, action_code, segment_special_requests, schedule_change_indicator, segment_booked_date, air_miles_flown, funnel_flight, change_of_gauge, flight_number, class_of_service, elapsed_time, equipment_type, eticket, number_in_party, code)
                if in_bound_connection == "false":  # begining of an itinerary
                    current_itinerary = Itinerary()
                    index = 0
                current_itinerary.addSegment(segment)
                if out_bound_connection == "false":  # end of an itinerary
                    list_itineraries.append(current_itinerary)
        return list_itineraries

    def _price_quote(self, price_quote):
        list_price_quote = []
        for price in ensureList(price_quote):
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

    def _forms_of_payment(self, forms_payment):
        list_forms_payment = []
        if forms_payment is None:
            return []
        for i in ensure_list(forms_payment):
            if 'stl18:CreditCardPayment' in i and 'ShortText' in i['stl18:CreditCardPayment']:
                form_of_payment = FormOfPayment(i['stl18:CreditCardPayment']['ShortText'])
                list_forms_payment.append(form_of_payment)
        return list_forms_payment

    def _ticketing(self, ticketing_info):
        list_ticket = []
        if "stl18:TicketDetails" not in ticketing_info:
            return []

        for ticket in ensureList(ticketing_info["stl18:TicketDetails"]):
            ticket_number = ticket["stl18:TicketNumber"]
            transaction_indicator = ticket["stl18:TransactionIndicator"]
            passenger_name = ticket["stl18:PassengerName"]
            agency_location = ticket["stl18:AgencyLocation"]
            time_stamp = ticket["stl18:Timestamp"]
            ticket_object = TicketingInfo_(ticket_number, transaction_indicator, passenger_name, agency_location, time_stamp)
            list_ticket.append(ticket_object)

        return list_ticket

    def _remarks(self, remarks):
        list_remarks = []
        for remark in ensureList(remarks):
            remark_index = remark['index']
            remark_type = remark['type']
            remark_id = remark['elementId']
            remark_text = remark['stl18:RemarkLines']['stl18:RemarkLine']['stl18:Text']
            remark_objet = Remarks(remark_index, remark_type, remark_id, remark_text)
            list_remarks.append(remark_objet)
        return list_remarks

    def _passengers(self, passengers):
        
        passenger_list = []

        for pax in ensureList(passengers):
            name_id = pax['nameId']
            pax_type = pax['passengerType']
            last_name = pax['stl18:LastName']
            first_name = pax['stl18:FirstName']
            full_name = f"{pax['stl18:FirstName']} {pax['stl18:LastName']}"

            if 'stl18:APISRequest' in pax['stl18:SpecialRequests']:
                if pax['passengerType'] != "INF" or  pax['passengerType'] != "JNF":
                    for i in ensureList(pax['stl18:SpecialRequests']['stl18:APISRequest']):
                        if full_name == f"{i['stl18:DOCSEntry']['stl18:Forename']} {i['stl18:DOCSEntry']['stl18:Surname']}":
                            date_of_birth = i['stl18:DOCSEntry']['stl18:DateOfBirth']
                            gender = i['stl18:DOCSEntry']['stl18:Gender']
                            number_in_party = i['stl18:DOCSEntry']['stl18:NumberInParty']

            else:
                for i in ensureList(passengers):
                    if 'withInfant' in i and i['withInfant'] == "true" and 'stl18:APISRequest' in i['stl18:SpecialRequests']:
                        for j in ensureList(i['stl18:SpecialRequests']['stl18:APISRequest']):
                            if full_name == f"{j['stl18:DOCSEntry']['stl18:Forename']} {j['stl18:DOCSEntry']['stl18:Surname']}":
                                date_of_birth = j['stl18:DOCSEntry']['stl18:DateOfBirth']
                                gender = j['stl18:DOCSEntry']['stl18:Gender']
                                number_in_party = j['stl18:DOCSEntry']['stl18:NumberInParty']

            p = Passenger(name_id, first_name, last_name, date_of_birth, gender, "", "", "", "", number_in_party, "", pax_type)
            passenger_list.append(p)
        return passenger_list
