from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core import xmlparser
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml, ensureList, fareTypePriceQuote
import logging
from pygds.core.sessions import SessionInfo
from pygds.core.price import AirItineraryPricingInfo, SearchPriceInfos, FareBreakdown
from pygds.core.ticket import TicketReply
from pygds.core.end_transaction import EndTransaction
from pygds.core.queue_place import QueuePlace
import re
from pygds.core.types import SendCommand, Passenger, PriceQuote_, FormatPassengersInPQ, FormatAmount, Itinerary, FlightSegment, FlightPointDetails, FormOfPayment, Remarks, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, TicketingInfo_


class BaseResponseExtractor(object):
    """
        This is a base class for all response extractor. A helpful class to extract useful info from an XML.
    """

    def __init__(self, xml_content: str, parse_session: bool = True, parse_app_error: bool = True,
                 main_tag: str = None):
        """
        constructor for base class
        :param xml_content: The content as XML
        :param parse_session: A boolean to tell if we will the session part
        :param parse_app_error: A boolean to tell if we will parse application error part
        :param main_tag: The main tag of the reply
        """
        self.xml_content = xml_content
        self.tree = None
        self.parsed = False
        self.parse_session = parse_session
        self.parse_app_error = parse_app_error
        self.main_tag = main_tag
        self.log = logging.getLogger(str(self.__class__))
        self.session_info: SessionInfo = None
        self.app_error: ApplicationError = None

    def default_value(self):
        return None

    def parse(self):
        """
            If not already done, it parses the XML content to JSON and save it.
        """
        if not self.parsed:
            self.tree = xmlparser.parse_xml(self.xml_content)
            self.parsed = True

    def extract(self):
        """
        The public method to call when extracting useful data.
        :return: GdsResponse
        """
        self.parse()
        if self.parse_app_error and self.app_error is None:
            self.app_error = AppErrorExtractor(self.xml_content, self.main_tag).extract().application_error
        return GdsResponse(None, self.default_value() if self.app_error else self._extract(), self.app_error)

    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class AppErrorExtractor(BaseResponseExtractor):
    """
    Extract application error from response
    """

    def __init__(self, xml_content: str, main_tag: str):
        super().__init__(xml_content, False, False, main_tag)
        self.parsed = True

    def extract(self):
        response = super().extract()
        response.application_error = response.payload
        return response

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", self.main_tag)
        app_error_data = from_json_safe(payload, "stl:ApplicationResults", "stl:Error")
        if not app_error_data:
            return None

        description = from_json_safe(app_error_data, "stl:SystemSpecificResults", "stl:Message")
        return ApplicationError(None, None, None, description)


class PriceSearchExtractor(BaseResponseExtractor):
    """
        Class to extract price search information from XML Response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="OTA_AirPriceRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body",
                           "OTA_AirPriceRS")
        status = from_json(payload, "stl:ApplicationResults", "@status")
        air_itinerary_pricing = from_json(payload, "PriceQuote", "PricedItinerary", "AirItineraryPricingInfo")
        air_itinerary_pricing = ensure_list(air_itinerary_pricing)
        air_itinerary_pricing_list = []
        for air_itinerary_pricing_inf in air_itinerary_pricing:
            passengers = self._get_passengers(air_itinerary_pricing_inf)
            air_itinerary_pricing_list.append(passengers)
        search_price_infos = SearchPriceInfos()
        search_price_infos.status = status
        search_price_infos.air_itinerary_pricing_info = air_itinerary_pricing_list
        return search_price_infos

    def _get_passengers(self, air_itinerary_pricing):

        for i in ensure_list(from_json(air_itinerary_pricing, "PassengerTypeQuantity")):

            itin_totalfare = from_json(air_itinerary_pricing, "ItinTotalFare")
            air_itinerary_pricing_info = AirItineraryPricingInfo()
            air_itinerary_pricing_info.base_fare = from_json(itin_totalfare, "EquivFare", "@Amount") if "EquivFare" in itin_totalfare else from_json(itin_totalfare, "BaseFare", "@Amount")
            air_itinerary_pricing_info.taxes = from_json(itin_totalfare, "Taxes", "@TotalAmount")
            air_itinerary_pricing_info.total_fare = from_json(itin_totalfare, "TotalFare", "@Amount")
            air_itinerary_pricing_info.currency_code = from_json(itin_totalfare, "TotalFare", "@CurrencyCode")
            air_itinerary_pricing_info.passenger_type = from_json(i, "@Code")
            air_itinerary_pricing_info.passenger_quantity = from_json(i, "@Quantity")
            air_itinerary_pricing_info.charge_amount = from_json(air_itinerary_pricing, "ItinTotalFare", "TotalFare", "@Amount")
            air_itinerary_pricing_info.tour_code = self._get_tour_code(air_itinerary_pricing)
            air_itinerary_pricing_info.ticket_designator = self._get_get_ticket_designator(air_itinerary_pricing)
            air_itinerary_pricing_info.commission_percentage = self._get_commission_percent(air_itinerary_pricing)
            air_itinerary_pricing_info.fare_break_down = self._get_fare_break_down(air_itinerary_pricing)

            return air_itinerary_pricing_info

    def _get_tour_code(self, air_itinerary_pricing):
        result = None
        if "Endorsements" in from_json(air_itinerary_pricing, "ItinTotalFare") and from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text"):
            text = from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text")
            if 'TC' in text:
                text = re.findall("TC ([0-9A-Z]+)", str)[0]
                result = text
        return result

    def _get_get_ticket_designator(self, air_itinerary_pricing):
        result = None
        if "Endorsements" in from_json(air_itinerary_pricing, "ItinTotalFare") and from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text"):
            text = from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text")
            if 'TD' in text:
                text = re.findall("TD ([0-9A-Z]+)", str)[0]
                result = text
        return result

    def _get_commission_percent(self, air_itinerary_pricing):
        result = 0

        if "PTC_FareBreakdown" in air_itinerary_pricing and isinstance(from_json(air_itinerary_pricing, "PTC_FareBreakdown"), list) and len(from_json(air_itinerary_pricing, "PTC_FareBreakdown")) > 0:
            fare_breakdown = from_json(air_itinerary_pricing, "PTC_FareBreakdown")
            text = from_json(fare_breakdown[0], "FareBasis", "@Code")
            if 'CM' in text:
                text = re.findall("CM([0-9]+)", text)[0]
                result = text
        return result

    def _get_fare_break_down(self, air_itinerary_pricing):

        fare_breakdown = FareBreakdown()
        fare_break_list = ensure_list(from_json(air_itinerary_pricing, "PTC_FareBreakdown"))
        fare_breakdown_list = []
        for fare_break in fare_break_list:
            fare_breakdown.cabin = from_json(fare_break, "Cabin")
            fare_breakdown.fare_basis_code = from_json(fare_break, "FareBasis", "@Code")
            fare_breakdown.fare_amount = from_json(fare_break, "FareBasis", "@FareAmount") if "@FareAmount" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.fare_passenger_type = from_json(fare_break, "FareBasis", "@FarePassengerType") if "@FarePassengerType" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.fare_type = from_json(fare_break, "FareBasis", "@FareType") if "@FareType" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.filing_carrier = from_json(fare_break, "FareBasis", "@FilingCarrier") if "@FilingCarrier" in from_json(fare_break, "FareBasis") else None

            fare_breakdown_list.append(fare_breakdown)

        return fare_breakdown_list


class IssueTicketExtractor(BaseResponseExtractor):
    """
        Class to extract issue ticket information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="AirTicketRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        response_data = from_json_safe(payload, "AirTicketRS")
        application_result_data = from_json_safe(response_data, "stl:ApplicationResults")
        status = from_json_safe(application_result_data, "@status")
        if status == "Complete":
            message_text = from_json_safe(response_data, "@Text")
            short_text = ""
            type_response = "Success"
        elif status == "NotProcessed":
            error_data = from_json_safe(application_result_data, "stl:Error")
            if error_data is not None:
                type_response = from_json_safe(error_data, "@type")
                system_specific_results_error = from_json_safe(error_data, "stl:SystemSpecificResults")
                message_text = from_json_safe(system_specific_results_error, "stl:Message")
                short_text = from_json_safe(system_specific_results_error, "stl:ShortText")
        else:
            message_text, short_text, type_response = (None, None, None)
        return TicketReply(status, type_response, message_text, short_text, "", "")


class EndTransactionExtractor(BaseResponseExtractor):
    """
        Class to extract end transaction information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="EndTransactionRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        response_data = from_json_safe(payload, "EndTransactionRS")
        status = from_json_safe(response_data, "stl:ApplicationResults", "@status")
        itinerary_ref = from_json_safe(response_data, "ItineraryRef")
        id_ref = from_json_safe(itinerary_ref, "ID")
        create_date_time = from_json_safe(itinerary_ref, "Source", "CreateDateTime")
        text_message = from_json_safe(response_data, "Text")
        return EndTransaction(status, id_ref, create_date_time, text_message)


class SabreReservationFormatter(BaseResponseExtractor):

    """
        A class to extract Reservation from response of retrieve PNR.
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="stl18:GetReservationRS")
        self.parsed = True

    def _extract(self):

        display_pnr = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "stl18:GetReservationRS")
        display_pnr = str(display_pnr).replace("@", "")
        display_pnr = eval(display_pnr.replace("u'", "'"))
        passengers_reservation = from_json(display_pnr, "stl18:Reservation", "stl18:PassengerReservation")
        return {
            'passengers': self._passengers(from_json(passengers_reservation, "stl18:Passengers", "stl18:Passenger")),
            'itineraries': self._itineraries(from_json(passengers_reservation, "stl18:Segments")),
            'form_of_payments': self._forms_of_payment(from_json(passengers_reservation, "stl18:FormsOfPayment")),
            'price_quotes': self._price_quote(from_json(display_pnr["or112:PriceQuote"]["PriceQuoteInfo"])),
            'ticketing_info': self._ticketing(from_json(passengers_reservation, "stl18:Passengers", "stl18:Passenger")),
            'remarks': self._remarks(from_json(display_pnr['stl18:Reservation']['stl18:Remarks']["stl18:Remark"])),
            'dk_number': from_json(display_pnr, "stl18:Reservation", "stl18:DKNumbers", "stl18:DKNumber")
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

            for i in ensureList(price_quote["Summary"]["NameAssociation"]):
                if pq_number == i["PriceQuote"]["number"]:
                    name_number = i["nameNumber"]
                    passenger_type = i["PriceQuote"]["Passenger"]["requestedType"]
                    passenger = FormatPassengersInPQ(name_number, passenger_type).to_data()
                    list_passengers.append(passenger)

            price_quote_data = PriceQuote_(pq_number, status, fare_type, base_fare, total_fare, tax_fare, list_passengers)
            list_price_quote.append(price_quote_data)

        return list_price_quote

    def _forms_of_payment(self, forms_payment):
        list_forms_payment = []
        if forms_payment is None:
            return []
        for i in ensure_list(forms_payment):
            if 'stl18:CreditCardPayment' in i and 'ShortText' in i['stl18:CreditCardPayment']:
                form_of_payment = FormOfPayment("", i['stl18:CreditCardPayment']['ShortText'], "", "", "")
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


class SabreSendCommandFormat(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="SabreCommandLLSRS")
        self.parsed = True

    def _extract(self):

        send_command = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "SabreCommandLLSRS")
        return {
            'command': self._send_command(from_json(send_command, "Response")),
        }

    def _send_command(self, command_response):

        return SendCommand(command_response)


class SabreQueuePlaceExtractor(BaseResponseExtractor):
    """
        Class to extract Queue Place information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="QueuePlaceRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        response_data = from_json_safe(payload, "QueuePlaceRS")
        application_result_data = from_json_safe(response_data, "stl:ApplicationResults")
        status = from_json_safe(application_result_data, "@status")
        if status == "Complete":
            message_text = from_json_safe(response_data, "Text")
            type_response = "Success"
        elif status == "NotProcessed":
            error_data = from_json_safe(application_result_data, "stl:Error")
            if error_data is not None:
                type_response = from_json_safe(error_data, "type")
                system_specific_results_error = from_json_safe(error_data, "stl:SystemSpecificResults")
                message_text = from_json_safe(system_specific_results_error, "stl:Message")
            else:
                message_text, type_response, type_response = (None, None, None)
        return QueuePlace(status, type_response, message_text)
class SendRemarkExtractor(BaseResponseExtractor):

    """Class to extract the send remark from XML response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="PassengerDetailsRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "PassengerDetailsRS")
        status = from_json(payload, "ApplicationResults", "@status")
        return {'status': status}
