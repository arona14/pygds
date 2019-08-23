from pygds.core.app_error import ApplicationError
from pygds.core.sessions import SessionInfo
from pygds.core.types import Passenger
from pygds.core.types import PriceQuote_, FormatPassengersInPQ, FormatAmount, Itinerary, FlightPriceQuote, FlightSummary, FlightAmounts, FlightPassenger_pq, FlightSegment, FlightPointDetails, FormOfPayment, TicketingInfo, Remarks, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, PriceQuote,TicketingInfo_
from pygds.sabre.helpers import get_data_from_json as from_json
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list,get_data_from_xml as from_xml, reformat_date,ensureList

from pygds.core.types import Itinerary, FlightPriceQuote, FlightSummary, FlightAmounts, FlightPassenger_pq, FlightSegment, FlightPointDetails, FormOfPayment, Remarks, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, PriceQuote, TicketingInfo_
from pygds.core.helpers import get_data_from_xml as from_xml, ensureList, ensure_list

def fareTypePriceQuote(passenger_type):
    fare_type = ""
    passenger_pub_list = ["ADT","CNN","C11","C10","C09","C08","C07","C06","C05","C04","C03","C02","INF"]
    if str(passenger_type).startswith("J") or str(passenger_type) not in passenger_pub_list:
        fare_type = "NET"
    else:
        fare_type = "PUB"
    return fare_type

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

    """
        A class to extract Reservation from response of retrieve PNR.
    """
    
    def __init__(self, xml_content: str):
        self.xml_content = xml_content

    def _extract(self):

        display_pnr = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "stl18:GetReservationRS")
        display_pnr = str(display_pnr).replace("@", "")
        display_pnr = eval(display_pnr.replace("u'", "'"))
        return {
            'passengers': self._passengers(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:Passengers']['stl18:Passenger']),
            'itineraries': self._itineraries(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:Segments']),
            'form_of_payments': self._forms_of_payment(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:FormsOfPayment']),
            'price_quotes': self._price_quote(display_pnr["or112:PriceQuote"]["PriceQuoteInfo"]),
            'ticketing_info': self._ticketing(display_pnr['stl18:Reservation']['stl18:PassengerReservation']['stl18:Passengers']['stl18:Passenger']),
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
                markting_short_name = i['stl18:Air']['stl18:MarktingAirlineShortName'] if 'stl18:MarktingAirlineShortName' in i['stl18:Air'] else ""
                marketing_airline_code = i['stl18:Air']['stl18:MarketingAirlineCode']
                equipment_type = i['stl18:Air']['stl18:EquipmentType']
                departure_terminal_code = i['stl18:Air']['stl18:DepartureTerminalCode'] if 'stl18:DepartureTerminalCode' in i['stl18:Air'] else ""
                arrival_terminal_code = i['stl18:Air']['stl18:ArrivalTerminalCode'] if 'stl18:ArrivalTerminalCode' in i['stl18:Air'] else ""
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
                elapsed_time = i['stl18:Air']['stl18:ElapsedTime'] if 'stl18:ElapsedTime' in i['stl18:Air'] else ""
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
        for price in ensureList(price_quote["Details"]):
            list_passengers = []
            pq_number = price["number"]
            status = price["status"]
            fare_type = fareTypePriceQuote(price["passengerType"])
            base_fare_value = price["FareInfo"]["BaseFare"]["#text"]
            base_fare_cc = price["FareInfo"]["BaseFare"]["currencyCode"]
            base_fare = FormatAmount(base_fare_value, base_fare_cc).to_data()

            total_fare_value = price["FareInfo"]["TotalFare"]["#text"]
            total_fare_cc = price["FareInfo"]["TotalFare"]["currencyCode"]
            total_fare = FormatAmount(total_fare_value, total_fare_cc).to_data()

            tax_fare_value = price["FareInfo"]["TotalTax"]["#text"]
            tax_fare_cc = price["FareInfo"]["TotalTax"]["currencyCode"]
            tax_fare = FormatAmount(tax_fare_value, tax_fare_cc).to_data()
            print(tax_fare)

            for i in ensureList(price_quote["Summary"]["NameAssociation"]):
                if pq_number == i["PriceQuote"]["number"]:
                    name_number = i["nameNumber"]
                    passenger_type = i["PriceQuote"]["Passenger"]["requestedType"]
                    passenger = FormatPassengersInPQ(name_number,passenger_type).to_data()
                    list_passengers.append(passenger)
                    
            price_quote_data = PriceQuote_(pq_number,status,fare_type,base_fare,total_fare,tax_fare,list_passengers)
            #pq_number: int = None,status: str = None, fare_type: str = None, base_fare=None, total_fare=None, total_tax=None, passengers=None
            list_price_quote.append(price_quote_data)

        return list_price_quote

    def _forms_of_payment(self, forms_payment):
        list_forms_payment = []
        if forms_payment is None:
            return []
        for i in ensure_list(forms_payment):
            if 'stl18:CreditCardPayment' in i and 'ShortText' in i['stl18:CreditCardPayment']:
                form_of_payment = FormOfPayment(i['stl18:CreditCardPayment']['ShortText'])
                list_forms_payment.append(form_of_payment)
        return list_forms_payment

    def _ticketing(self, passengers):
        list_ticket = []
        if "stl18:TicketingInfo" not in passengers:
            return []
        for pax in ensureList(passengers):
            name_id = pax['nameId']
            for ticket in ensureList(passengers["stl18:TicketingInfo"]["stl18:TicketDetails"]):
                ticket_number = ticket["stl18:TicketNumber"]
                transaction_indicator = ticket["stl18:TransactionIndicator"]
                name_number = name_id
                agency_location = ticket["stl18:AgencyLocation"]
                time_stamp = ticket["stl18:Timestamp"]
                ticket_object = TicketingInfo_(ticket_number, transaction_indicator, name_number, agency_location, time_stamp)
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
                if pax['passengerType'] != "INF" or pax['passengerType'] != "JNF":
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
