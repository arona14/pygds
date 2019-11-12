import logging
import re
from typing import List

from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core import xmlparser
from pygds.core.app_error import ApplicationError
from pygds.core.exchange import (BaggageInfo, BaseFare, BookItinerary,
                                 ExchangeAirItineraryPricingInfo,
                                 ExchangeComparison, ExchangeComparisonInfos,
                                 ExchangeConfirmationInfos, ExchangeData,
                                 ExchangeDetails, ExchangeFlightSegment,
                                 ExchangeShoppingInfos, Fare, ItinTotalFare,
                                 MarketingAirline, OriginDestination,
                                 PriceDifference, ReservationSegment,
                                 SourceData, TaxComparison, TaxData,
                                 TotalPriceDifference)
from pygds.core.helpers import ensure_list
from pygds.core.helpers import get_data_from_json as from_json
from pygds.core.helpers import get_data_from_json_safe as from_json_safe
from pygds.core.helpers import get_data_from_xml as from_xml
from pygds.core.price import (AirItineraryPricingInfo, FareBreakdown,
                              SearchPriceInfos)
from pygds.core.rebook import RebookInfo
from pygds.core.sessions import SessionInfo
from pygds.core.ticket import TicketReply
from pygds.core.types import (Agent, CabinClass, CabinInfo, ColumnInfo,
                              ElectronicDocument, EndTransaction, FaciltyInfo,
                              FlightAirlineDetails, FlightDisclosureCarrier,
                              FlightInfo, FlightMarriageGrp,
                              FlightPointDetails, FlightSegment, FormatAmount,
                              FormatPassengersInPQ, IgnoreTransaction,
                              InfoPayment, Itinerary, OperatingMarketing,
                              Passenger, PriceQuote_, QueuePlace, Remarks,
                              RowFacilityInfo, RowInfo, SeatInfo, SeatMap,
                              SendCommand, ServiceCoupon, TicketDetails,
                              TicketingInfo_, TypeInfo, Offer, BasePrice, TotalAmount, Taxes)


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


class SabreSoapErrorExtractor(BaseResponseExtractor):
    """
        Extractor for error
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, True, False)

    def _extract(self):
        return xmlparser.extract_single_elements(self.tree, "//faultcode/text()", "//faultstring/text()")


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
            app_error_data = from_json_safe(payload, "stl18:Errors", "stl18:Error")
            if not app_error_data:
                return None
            error_code = from_json_safe(app_error_data, "stl18:Code")
            error_message = from_json_safe(app_error_data, "stl18:Message")
            error_category = from_json_safe(app_error_data, "stl18:Severity")
            return ApplicationError(error_code, error_category, None, error_message)

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
        status = from_json_safe(payload, "stl:ApplicationResults", "@status")
        air_itinerary_pricing = from_json_safe(payload, "PriceQuote", "PricedItinerary", "AirItineraryPricingInfo")
        validating_carrier = from_json_safe(payload, "PriceQuote", "MiscInformation", "HeaderInformation", "ValidatingCarrier", "@Code")
        air_itinerary_pricing = ensure_list(air_itinerary_pricing)
        air_itinerary_pricing_list = []
        for air_itinerary_pricing_inf in air_itinerary_pricing:
            passengers = self._get_passengers(air_itinerary_pricing_inf, validating_carrier)
            air_itinerary_pricing_list.append(passengers)
        search_price_infos = SearchPriceInfos()
        search_price_infos.status = status
        search_price_infos.air_itinerary_pricing_info = air_itinerary_pricing_list
        return search_price_infos

    def _get_passengers(self, air_itinerary_pricing, validating_carrier):

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
            air_itinerary_pricing_info.tour_code = self._get_tour_code_or_ticket_designator(air_itinerary_pricing, 'TC')
            air_itinerary_pricing_info.ticket_designator = self._get_tour_code_or_ticket_designator(air_itinerary_pricing, 'TD')
            air_itinerary_pricing_info.commission_percentage = self._get_commission_percent(air_itinerary_pricing)
            air_itinerary_pricing_info.fare_break_down = self._get_fare_break_down(air_itinerary_pricing)
            air_itinerary_pricing_info.valiating_carrier = validating_carrier
            air_itinerary_pricing_info.baggage_provisions = from_json(air_itinerary_pricing, "BaggageProvisions")

            return air_itinerary_pricing_info

    def _get_tour_code_or_ticket_designator(self, air_itinerary_pricing, code):
        result = None
        if "Endorsements" in from_json(air_itinerary_pricing, "ItinTotalFare") and from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text"):
            text = from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text")
            if code in text:
                text = re.findall(code + " ([0-9A-Z]+)", text)[0]
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

        fare_break_list = ensure_list(from_json(air_itinerary_pricing, "PTC_FareBreakdown"))
        fare_breakdown_list = []
        for fare_break in fare_break_list:
            fare_breakdown = FareBreakdown()
            fare_breakdown.cabin = from_json(fare_break, "Cabin")
            fare_breakdown.fare_basis_code = from_json(fare_break, "FareBasis", "@Code")
            fare_breakdown.fare_amount = from_json(fare_break, "FareBasis", "@FareAmount") if "@FareAmount" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.fare_passenger_type = from_json(fare_break, "FareBasis", "@FarePassengerType") if "@FarePassengerType" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.fare_type = from_json(fare_break, "FareBasis", "@FareType") if "@FareType" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.filing_carrier = from_json(fare_break, "FareBasis", "@FilingCarrier") if "@FilingCarrier" in from_json(fare_break, "FareBasis") else None
            fare_breakdown.free_baggage = from_json(fare_break, "FreeBaggageAllowance") if "FreeBaggageAllowance" in from_json(fare_break) else None

            fare_breakdown_list.append(fare_breakdown)

        return fare_breakdown_list


class RebookExtractor(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="EnhancedAirBookRS")
        self.parsed = True

    def _extract(self):
        rebook_info = RebookInfo()
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "EnhancedAirBookRS")
        rebook_info.status = from_json(payload, "ApplicationResults", "@status")
        air_book = from_json_safe(payload, "OTA_AirBookRS")
        rebook_info.air_book_rs = air_book if air_book is not None else {}
        travel_itinerary = from_json_safe(payload, "TravelItineraryReadRS")
        rebook_info.travel_itinerary_read_rs = travel_itinerary if travel_itinerary is not None else {}
        return rebook_info


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


class DisplayPnrExtractor(BaseResponseExtractor):
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
        passengers_reservation = from_json_safe(display_pnr, "stl18:Reservation", "stl18:PassengerReservation")
        remarks = self._remarks(from_json_safe(display_pnr, "stl18:Reservation", "stl18:Remarks", "stl18:Remark"))
        return {
            'passengers': self._passengers(from_json_safe(passengers_reservation, "stl18:Passengers", "stl18:Passenger")),
            'itineraries': self._itineraries(from_json_safe(passengers_reservation, "stl18:Segments")),
            'form_of_payments': self.list_fop(remarks),
            'price_quotes': self._price_quote(from_json_safe(display_pnr, "or112:PriceQuote", "PriceQuoteInfo")),
            'ticketing_info': self._ticketing(from_json_safe(passengers_reservation, "stl18:Passengers", "stl18:Passenger")),
            'remarks': remarks,
            'dk_number': from_json_safe(display_pnr, "stl18:Reservation", "stl18:DKNumbers", "stl18:DKNumber"),
            'record_locator': from_json_safe(display_pnr, "stl18:Reservation", "stl18:BookingDetails", "stl18:RecordLocator")
        }

    def fare_type_price_quote(self, passenger_type):
        fare_type = ""
        passenger_pub_list = ["ADT", "CNN", "C11", "C10", "C09", "C08", "C07", "C06", "C05", "C04", "C03", "C02", "INF"]
        if str(passenger_type).startswith("J") or str(passenger_type) not in passenger_pub_list:
            fare_type = "NET"
        else:
            fare_type = "PUB"
        return fare_type

    def _itineraries(self, itinerary):

        if itinerary is None:
            return []
        list_itineraries = []  # list of itineraries
        current_itinerary = None
        index = 0
        for i in ensure_list(from_json(itinerary, "stl18:Segment")):
            if 'stl18:Air' in i:
                air_segment = from_json(i, "stl18:Air")
                if 'Code' in i['stl18:Air']:
                    code = from_json_safe(air_segment, "Code")
                else:
                    code = ""
                res_book_desig_code = from_json_safe(air_segment, "ResBookDesigCode")
                code_disclosure_carrier = ""
                dot = ""
                banner = ""
                ind = from_json_safe(air_segment, "stl18:MarriageGrp", "stl18:Ind")
                group = from_json_safe(air_segment, "stl18:MarriageGrp", "stl18:Group")
                sequence = from_json_safe(air_segment, "stl18:MarriageGrp", "stl18:Sequence")
                depart_airport = from_json_safe(air_segment, "stl18:DepartureAirport")
                arrival_airport = from_json_safe(air_segment, "stl18:ArrivalAirport")
                operating_airline_code = from_json_safe(air_segment, "stl18:OperatingAirlineCode")
                operating_short_name = from_json_safe(air_segment, "stl18:OperatingAirlineShortName")
                markting_short_name = from_json_safe(air_segment, "stl18:MarktingAirlineShortName") if "stl18:MarktingAirlineShortName" in air_segment else ""
                marketing_airline_code = from_json_safe(air_segment, "stl18:MarketingAirlineCode")
                equipment_type = from_json_safe(air_segment, "stl18:EquipmentType")
                departure_terminal_code = from_json_safe(air_segment, "stl18:DepartureTerminalCode") if "stl18:DepartureTerminalCode" in air_segment else ""
                arrival_terminal_code = from_json_safe(air_segment, "stl18:ArrivalTerminalCode") if "stl18:ArrivalTerminalCode" in air_segment else ""
                eticket = from_json_safe(air_segment, "stl18:Eticket")
                departure_date_time = from_json_safe(air_segment, "stl18:DepartureDateTime")
                arrival_date_time = from_json_safe(air_segment, "stl18:ArrivalDateTime")
                flight_number = from_json_safe(air_segment, "stl18:FlightNumber")
                markting_flight_number = from_json_safe(air_segment, "stl18:MarketingFlightNumber")
                operating_flight_number = from_json_safe(air_segment, "stl18:OperatingFlightNumber")
                class_of_service = from_json_safe(air_segment, "stl18:ClassOfService")
                operating_class_of_service = from_json_safe(air_segment, "stl18:OperatingClassOfService")
                markting_class_of_service = from_json_safe(air_segment, "stl18:MarketingClassOfService")
                number_in_party = from_json_safe(air_segment, "stl18:NumberInParty")
                out_bound_connection = from_json_safe(air_segment, "stl18:outboundConnection")
                in_bound_connection = from_json_safe(air_segment, "stl18:inboundConnection")
                airline_ref_id = str(from_json_safe(air_segment, "stl18:AirlineRefId")).split('*')[1]
                elapsed_time = from_json_safe(air_segment, "stl18:ElapsedTime") if "stl18:ElapsedTime" in air_segment else ""
                seats = from_json_safe(air_segment, "stl18:Seats")
                segment_special_requests = from_json_safe(air_segment, "stl18:SegmentSpecialRequests")
                schedule_change_indicator = from_json_safe(air_segment, "stl18:ScheduleChangeIndicator")
                segment_booked_date = from_json_safe(air_segment, "stl18:SegmentBookedDate")
                air_miles_flown = from_json_safe(air_segment, "stl18:AirMilesFlown")
                funnel_flight = from_json_safe(air_segment, "stl18:FunnelFlight")
                change_of_gauge = from_json_safe(air_segment, "stl18:ChangeOfGauge")
                action_code = from_json_safe(air_segment, "stl18:ActionCode")
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
                current_itinerary.addSegment(segment)
                if out_bound_connection == "false":  # end of an itinerary
                    list_itineraries.append(current_itinerary)
        return list_itineraries

    def _price_quote(self, price_quote):

        list_price_quote = []
        for price in ensure_list(from_json(price_quote, "Details")):
            list_passengers = []
            pq_number = from_json_safe(price, "number")
            status = from_json_safe(price, "status")
            fare_type = self.fare_type_price_quote(from_json_safe(price, "passengerType"))
            if "EquivalentFare" in from_json_safe(price, "FareInfo"):
                base_fare_value = from_json_safe(price, "FareInfo", "EquivalentFare", "#text")
                base_fare_cc = from_json_safe(price, "FareInfo", "EquivalentFare", "currencyCode")
            else:
                base_fare_value = float(from_json_safe(price, "FareInfo", "BaseFare", "#text"))
                base_fare_cc = from_json_safe(price, "FareInfo", "BaseFare", "currencyCode")
            base_fare = FormatAmount(base_fare_value, base_fare_cc).to_data()

            total_fare_value = float(from_json_safe(price, "FareInfo", "TotalFare", "#text"))
            total_fare_cc = from_json_safe(price, "FareInfo", "TotalFare", "currencyCode")
            total_fare = FormatAmount(total_fare_value, total_fare_cc).to_data()

            tax_fare_value = float(from_json_safe(price, "FareInfo", "TotalTax", "#text"))
            tax_fare_cc = from_json_safe(price, "FareInfo", "TotalTax", "currencyCode")
            tax_fare = FormatAmount(tax_fare_value, tax_fare_cc).to_data()
            validating_carrier = from_json_safe(price, "MiscellaneousInfo", "ValidatingCarrier")
            commission_percentage = from_json_safe(price, "FareInfo", "Commission", "Percentage")
            for i in ensure_list(price_quote["Summary"]["NameAssociation"]):
                if pq_number == from_json_safe(i, "PriceQuote", "number"):
                    name_number = from_json_safe(i, "nameNumber")
                    passenger_type = from_json_safe(i, "PriceQuote", "Passenger", "requestedType")
                    passenger = FormatPassengersInPQ(name_number, passenger_type).to_data()
                    list_passengers.append(passenger)

            price_quote_data = PriceQuote_(int(pq_number), status, fare_type, base_fare, total_fare, tax_fare, validating_carrier, list_passengers, commission_percentage)
            list_price_quote.append(price_quote_data)

        return list_price_quote

    def list_fop(self, remarks: List[Remarks]):
        """
        This function return the list of card_type, card_number and expirate date in the text of remark_type FOP
        :param: remark
        :return: list of card_type, card_number and expirate date

        """
        remarks = remarks or []
        objet_fop = []
        list_info = []
        for r in remarks:
            if r.type_remark == "FOP" and r.text == "CHECK":
                fop_type = "CK"
                info_payment = InfoPayment("", "", "", "", fop_type)
                list_info.append(info_payment)
            elif r.type_remark == "FOP":
                fop_type = "CC"
                objet_fop = r
                sort_tex = objet_fop.text
                expres = "([A-Z]{2})([0-9]+)¥([0-9]+)/([0-9]+)"
                extract_value = re.compile(expres)
                val_data = extract_value.findall(sort_tex)
                if len(val_data) > 0 and len(val_data[0]) > 3:
                    info_payment = InfoPayment(val_data[0][0], val_data[0][1], val_data[0][2], val_data[0][3], fop_type)
                    list_info.append(info_payment)
        return list_info

    def _ticketing(self, passengers):
        list_ticket = []
        for pax in ensure_list(passengers):
            if "stl18:TicketingInfo" not in pax:
                pass
            else:
                name_id = from_json(pax, "nameId")
                for ticket in ensure_list(from_json(pax, "stl18:TicketingInfo", "stl18:TicketDetails")):
                    ticket_number = from_json_safe(ticket, "stl18:TicketNumber")
                    transaction_indicator = from_json_safe(ticket, "stl18:TransactionIndicator")
                    agency_location = from_json_safe(ticket, "stl18:AgencyLocation")
                    time_stamp = from_json_safe(ticket, "stl18:Timestamp")
                    ticket_object = TicketingInfo_(ticket_number, transaction_indicator, name_id, agency_location, time_stamp)
                    list_ticket.append(ticket_object)

        return list_ticket

    def _remarks(self, remarks):
        list_remarks = []
        for remark in ensure_list(remarks):
            remark_index = from_json(remark, "index")
            remark_type = from_json(remark, "type")
            remark_id = from_json(remark, "elementId")
            remark_text = from_json(remark, "stl18:RemarkLines", "stl18:RemarkLine", "stl18:Text")
            remark_objet = Remarks(remark_index, remark_type, remark_id, remark_text)
            list_remarks.append(remark_objet)
        return list_remarks

    def _passengers(self, passengers):

        passenger_list = []

        for pax in ensure_list(passengers):
            name_id = from_json(pax, "nameId")
            pax_type = from_json(pax, "passengerType")
            last_name = from_json(pax, "stl18:LastName")
            first_name = from_json(pax, "stl18:FirstName")
            full_name = f"{first_name} {last_name}"

            if 'stl18:APISRequest' in from_json(pax, "stl18:SpecialRequests"):
                if pax_type != "INF" or pax_type != "JNF":
                    for i in ensure_list(from_json(pax, "stl18:SpecialRequests", "stl18:APISRequest")):
                        if full_name == f"""{from_json_safe(i, "stl18:DOCSEntry", "stl18:Forename")} {from_json_safe(i, "stl18:DOCSEntry", "stl18:Surname")}""":
                            date_of_birth = from_json_safe(i, "stl18:DOCSEntry", "stl18:DateOfBirth")
                            gender = from_json_safe(i, "stl18:DOCSEntry", "stl18:Gender")
                            number_in_party = from_json_safe(i, "stl18:DOCSEntry", "stl18:NumberInParty")

            else:
                for i in ensure_list(passengers):
                    if from_json_safe(i, "withInfant") == "true" and "stl18:APISRequest" in from_json(i, "stl18:SpecialRequests"):
                        for j in ensure_list(from_json(i, "stl18:SpecialRequests", "stl18:APISRequest")):
                            if full_name == f"""{from_json_safe(j, "stl18:DOCSEntry", "stl18:Forename")} {from_json_safe(j, "stl18:DOCSEntry", "stl18:Surname")}""":
                                date_of_birth = from_json_safe(j, "stl18:DOCSEntry", "stl18:DateOfBirth")
                                gender = from_json_safe(j, "stl18:DOCSEntry", "stl18:Gender")
                                number_in_party = from_json_safe(j, "stl18:DOCSEntry", "stl18:NumberInParty")

            p = Passenger(name_id, first_name, last_name, date_of_birth, gender, "", "", "", "", number_in_party, "", pax_type)
            passenger_list.append(p)
        return passenger_list


class SendCommandExtractor(BaseResponseExtractor):

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


class SabreIgnoreTransactionExtractor(BaseResponseExtractor):
    """
        Class to extract ignore transaction information from XML Response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="IgnoreTransactionRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        response_data = from_json_safe(payload, "IgnoreTransactionRS")
        application_results = from_json_safe(response_data, "stl:ApplicationResults")
        status = from_json_safe(application_results, "@status")
        create_date_time = from_json_safe(application_results, "stl:Success", "@timeStamp")
        return IgnoreTransaction(status, create_date_time)


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


class ExchangeBaseResponseExtractor(object):
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
            self.app_error = ExchangeAppErrorExtractor(self.xml_content, self.main_tag).extract().application_error
        return GdsResponse(None, self.default_value() if self.app_error else self._extract(), self.app_error)

    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class ExchangeAppErrorExtractor(ExchangeBaseResponseExtractor):
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
        payload = from_xml(self.xml_content, "SOAP-ENV:Envelope", "SOAP-ENV:Body", self.main_tag)
        app_error_data = from_json_safe(payload, "stl:ApplicationResults", "stl:Error")
        if not app_error_data:
            return None

        description = from_json_safe(app_error_data, "stl:SystemSpecificResults", "stl:Message")
        return ApplicationError(None, None, None, description)


class IsTicketExchangeableExtractor(ExchangeBaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="GetElectronicDocumentRS")
        self.parsed = True

    def _extract(self):

        payload = from_xml(self.xml_content, "SOAP-ENV:Envelope", "SOAP-ENV:Body")
        ticket_exchangeable_rs = from_json(payload, "GetElectronicDocumentRS")
        ticket_exchangeable_rs = str(ticket_exchangeable_rs).replace("@", "")
        ticket_exchangeable_rs = eval(ticket_exchangeable_rs.replace("u'", "'"))

        return {
            'is_ticket_exchangeable': self.is_ticket_exchangeable(ticket_exchangeable_rs)
        }

    def is_ticket_exchangeable(self, data):

        status = from_json(data, "STL:STL_Header.RS", "STL:Results")
        agent_data = from_json(data, "Agent")
        sine = from_json_safe(agent_data, "sine")
        ticketing_provider = from_json_safe(agent_data, "TicketingProvider")
        work_location = from_json_safe(agent_data, "WorkLocation")
        home_location = from_json_safe(agent_data, "HomeLocation")
        iso_country_code = from_json_safe(agent_data, "IsoCountryCode")
        agent_ = Agent(sine, ticketing_provider, work_location, home_location, iso_country_code)
        for t in ensure_list(from_json(data, "DocumentDetailsDisplay", "Ticket")):
            number = from_json(t, "number")
            traveler = from_json(t, "Customer", "Traveler")
            ticket_details = TicketDetails(number, traveler)
            for i in from_json_safe(t, "ServiceCoupon"):
                coupon = from_json(i, "coupon")
                marketing_provider = from_json(i, "MarketingProvider")
                marketing_flight_number = from_json(i, "MarketingFlightNumber")
                operating_provider = from_json(i, "OperatingProvider")
                origin = from_json(i, "StartLocation")
                destination = from_json(i, "EndLocation")
                class_of_service = from_json(i, "ClassOfService", "name")
                booking_status = from_json(i, "BookingStatus")
                current_status = from_json(i, "CurrentStatus")
                service_coupon = ServiceCoupon(coupon, marketing_provider, marketing_flight_number, operating_provider, origin, destination, class_of_service, booking_status, current_status)
                ticket_details.add_service_coupon(service_coupon)
        to_return = ElectronicDocument(status, agent_, ticket_details)

        return to_return


class ExchangeShoppingExtractor(BaseResponseExtractor):

    """
        A class to extract itineraries for ticket exchange
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="ExchangeShoppingRS")
        self.parsed = True

    def _extract(self):

        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        exchange_shopping_rs = from_json(payload, "ExchangeShoppingRS")
        exchange_shopping_rs = str(exchange_shopping_rs).replace("@", "")
        exchange_shopping_rs = eval(exchange_shopping_rs.replace("u'", "'"))
        status = from_json(exchange_shopping_rs, "ApplicationResults", "status")
        to_return = []
        for i in ensure_list(from_json(exchange_shopping_rs, "Solution")):
            sequence = from_json(i, "sequence")
            book_itinerary = self._book_itinerary(from_json(i, "BookItinerary"))
            fare = self._fare(from_json(i, "Fare"))
            exchange_data = ExchangeData(sequence, book_itinerary, fare)
            to_return.append(exchange_data)
        exchange_shopping = ExchangeShoppingInfos(status, to_return)
        return exchange_shopping

    def _book_itinerary(self, book_itinerary_data):

        book_iti = BookItinerary()
        for ori in ensure_list(from_json(book_itinerary_data, "OriginDestination")):
            origin_destination = OriginDestination()
            list_segment = []
            list_itinerary = []
            for book in ensure_list(from_json(ori, "ReservationSegment")):
                segment_number = from_json_safe(book, "segmentNumber")
                elapsed_time = from_json_safe(book, "elapsedTime")
                departure_date = from_json_safe(book, "startDateTime")
                arrival_date = from_json_safe(book, "endDateTime")
                origin = from_json_safe(book, "startLocation")
                destination = from_json_safe(book, "endLocation")
                marketing_flight_number = from_json_safe(book, "marketingFlightNumber")
                marketing = from_json_safe(book, "marketingProvider")
                operating = from_json_safe(book, "operatingProvider")
                reservation_segment = ReservationSegment(segment_number, elapsed_time, departure_date, arrival_date, origin, destination, marketing_flight_number, marketing, operating)
                list_segment.append(reservation_segment)
                origin_destination.segments = list_segment
                list_itinerary.append(origin_destination)
        book_iti.origin_destination = list_itinerary
        return book_iti

    def _fare(self, fare_data):
        valid = from_json(fare_data, "valid")
        sub_total_difference_currency_code = from_json_safe(fare_data, "TotalPriceDifference", "SubtotalDifference", "currencyCode")
        sub_total_difference_amount = from_json_safe(fare_data, "TotalPriceDifference", "SubtotalDifference", "#text")
        sub_total_difference = PriceDifference(sub_total_difference_currency_code, sub_total_difference_amount)

        total_fee_currency_code = from_json_safe(fare_data, "TotalPriceDifference", "TotalFee", "currencyCode")
        total_fee_difference_amount = from_json_safe(fare_data, "TotalPriceDifference", "TotalFee", "#text")
        total_fee = PriceDifference(total_fee_currency_code, total_fee_difference_amount)

        grand_total_difference_currency_code = from_json_safe(fare_data, "TotalPriceDifference", "GrandTotalDifference", "currencyCode")
        grand_total_difference_amount = from_json_safe(fare_data, "TotalPriceDifference", "GrandTotalDifference", "#text")
        grand_total_difference = PriceDifference(grand_total_difference_currency_code, grand_total_difference_amount)
        total_price = TotalPriceDifference(sub_total_difference, total_fee, grand_total_difference)
        to_return = Fare(valid, total_price)
        return to_return


class ExchangePriceExtractor(BaseResponseExtractor):

    """
        A class to extract Price from response of price an air ticket exchange.
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="AutomatedExchangesRS")
        self.parsed = True

    def _extract(self):

        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        automated_exchanges_rs = from_json(payload, "AutomatedExchangesRS")
        automated_exchanges_rs = str(automated_exchanges_rs).replace("@", "")
        automated_exchanges_rs = eval(automated_exchanges_rs.replace("u'", "'"))
        status = from_json(automated_exchanges_rs, "STL:ApplicationResults", "status")
        baggage = self._baggage_info(from_json(automated_exchanges_rs, "BaggageInfo"))
        comparaison = self._exchange_comparaison(from_json(automated_exchanges_rs, "ExchangeComparison"))
        to_return = ExchangeComparisonInfos(status, baggage, comparaison)
        return to_return

    def _baggage_info(self, baggage_data):

        list_flight_segment = []
        for i in ensure_list(from_json(baggage_data, "FlightSegment")):
            departure_date = from_json_safe(i, "DepartureDateTime")
            arrival_date = from_json_safe(i, "ArrivalDateTime")
            flight_number = from_json_safe(i, "FlightNumber")
            rph = from_json_safe(i, "RPH")
            segment_number = from_json_safe(i, "SegmentNumber")
            origin = from_json_safe(i, "OriginLocation", "LocationCode")
            destination = from_json_safe(i, "DestinationLocation", "LocationCode")
            marketing_airline_code = from_json_safe(i, "MarketingAirline", "Code")
            marketing_airline_flight_number = from_json_safe(i, "MarketingAirline", "FlightNumber")
            marketing_airline = MarketingAirline(marketing_airline_code, marketing_airline_flight_number)
            free_baggage_allowance = from_json_safe(i, "FreeBaggageAllowance", "Number")
            flight_segment = ExchangeFlightSegment(departure_date, arrival_date, origin, destination, flight_number, rph, segment_number, marketing_airline, free_baggage_allowance)
            list_flight_segment.append(flight_segment)
        baggage_info = BaggageInfo()
        baggage_info.flight_segment = list_flight_segment
        return baggage_info

    def _exchange_comparaison(self, exchange_comparaison_data):

        itinerary_pricing_list = []
        tax_comparaison_list = []

        for i in ensure_list(from_json(exchange_comparaison_data, "AirItineraryPricingInfo")):
            base_fare_amount = from_json_safe(i, "ItinTotalFare", "BaseFare", "Amount")
            base_fare_cc = from_json_safe(i, "ItinTotalFare", "BaseFare", "CurrencyCode")
            taxe = from_json_safe(i, "ItinTotalFare", "Taxes", "TotalAmount")
            total_fare = from_json_safe(i, "ItinTotalFare", "TotalFare", "Amount")
            base_fare = BaseFare(base_fare_amount, base_fare_cc)
            itin_total_fare = ItinTotalFare(base_fare, taxe, total_fare)
            price_type = from_json_safe(i, "Type")
            air_itinerary_pricing_info = ExchangeAirItineraryPricingInfo(price_type, itin_total_fare)
            itinerary_pricing_list.append(air_itinerary_pricing_info)

        for t in ensure_list(from_json(exchange_comparaison_data, "TaxComparison")):
            tax_type = from_json_safe(t, "Type")
            tax_list = []
            for t1 in ensure_list(from_json(t, "Tax")):
                tax_amount = from_json_safe(t1, "Amount")
                tax_code = from_json_safe(t1, "Amount")
                tax_data = TaxData(tax_amount, tax_code)
                tax_list.append(tax_data)
            tax_comparison = TaxComparison(tax_type, tax_list)
            tax_comparaison_list.append(tax_comparison)

        change_fee_collection = from_json(exchange_comparaison_data, "ExchangeDetails", "ChangeFeeCollectionOptions", "FeeCollectionMethod")
        exchange_reissue = from_json(exchange_comparaison_data, "ExchangeDetails", "ExchangeReissue")
        change_fee = from_json(exchange_comparaison_data, "ExchangeDetails", "ChangeFee")
        total_refund = from_json(exchange_comparaison_data, "ExchangeDetails", "TotalRefund")
        exchange_details = ExchangeDetails(change_fee, exchange_reissue, total_refund, change_fee_collection)
        pqr_number = from_json(exchange_comparaison_data, "ExchangeComparison", "PQR_Number")
        exchange_comparison = ExchangeComparison(pqr_number, exchange_details)
        exchange_comparison.air_itinerary_pricing_info = itinerary_pricing_list
        exchange_comparison.tax_comparison = tax_comparaison_list
        return exchange_comparison


class ExchangeCommitExtractor(BaseResponseExtractor):

    """
        A class to extract Reservation from response of retrieve PNR.
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="AutomatedExchangesRS")
        self.parsed = True

    def _extract(self):

        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        automated_exchanges_rs = from_json(payload, "AutomatedExchangesRS")
        automated_exchanges_rs = str(automated_exchanges_rs).replace("@", "")
        automated_exchanges_rs = eval(automated_exchanges_rs.replace("u'", "'"))

        status = self._source(from_json(automated_exchanges_rs, "STL:ApplicationResults", "status"))
        pqr_number = self._source(from_json(automated_exchanges_rs, "STL:ExchangeConfirmation", "PQR_Number"))
        source = self._source(from_json(automated_exchanges_rs, "Source"))
        exchange_confirmation = ExchangeConfirmationInfos(status, pqr_number, source)

        return {
            "exchange_confirmation": exchange_confirmation
        }

    def _source(self, source_data):

        agency_city = from_json_safe(source_data, "AgencyCity")
        agent_duty_sine = from_json_safe(source_data, "AgentDutySine")
        agent_work_area = from_json_safe(source_data, "AgentWorkArea")
        create_date_time = from_json_safe(source_data, "CreateDateTime")
        iata_number = from_json_safe(source_data, "IATA_Number")
        pseudo_city_code = from_json_safe(source_data, "PseudoCityCode")
        to_return = SourceData(agency_city, agent_duty_sine, agent_work_area, create_date_time, iata_number, pseudo_city_code)
        return to_return


class SeatMapResponseExtractor(BaseResponseExtractor):
    """
        Will extract response from seat map service
    """

    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "EnhancedSeatMapRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        seat_map = from_json_safe(payload, "EnhancedSeatMapRS", "SeatMap")
        if seat_map:
            change_of_gauge = seat_map["@changeOfGaugeInd"]
            equipment = seat_map["Equipment"]
            flight = self._get_flight_info(seat_map["Flight"])
            cabin = self._get_cabin_info(seat_map["Cabin"])
            seat = SeatMap(change_of_gauge, equipment, flight, cabin)
        else:
            seat = SeatMap(None, None, None, None)
        return seat

    def _get_flight_info(self, flight):
        """" In this method we get the seat map flight info
        :param: flight: dict of flight
        :return FlightInfo: the flight info class"""

        destination = from_json_safe(flight, "@destination")
        origin = from_json_safe(flight, "@origin")
        departure_date = from_json_safe(flight, "DepartureDate")
        departure_date = from_json_safe(flight, "DepartureDate", "#text") if "#text" in departure_date else departure_date
        carrier = from_json_safe(flight, "Marketing", "@carrier")
        code = from_json_safe(flight, "Marketing", "#text")
        operating = OperatingMarketing(carrier=carrier, code=code)
        marketing = OperatingMarketing(carrier=carrier, code=code)
        return FlightInfo(destination=destination, origin=origin, departure_date=departure_date, operating=operating, marketing=marketing)

    def _get_cabin_info(self, cabin):
        first_row = from_json_safe(cabin, "@firstRow")
        last_row = from_json_safe(cabin, "@lastRow")
        seat_occupation_default = from_json_safe(cabin, "@seatOccupationDefault") if "@seatOccupationDefault" in cabin else ''
        cabin_class = self.__get_cabin_class(from_json_safe(cabin, "CabinClass"))
        row = self.__get_row_info(from_json_safe(cabin, "Row"))
        column = self.__get_column_info(from_json_safe(cabin, "Column"))
        return CabinInfo(first_row=first_row, last_row=last_row, seat_occupation_default=seat_occupation_default, cabin_class=cabin_class, row=row, column=column)

    def __get_cabin_class(self, cabin_class):
        cabin_type = from_json_safe(cabin_class, "CabinType") if "CabinType" in cabin_class else ''
        class_of_service = from_json_safe(cabin_class, "RBD")
        marketing_description = from_json_safe(cabin_class, "MarketingDescription") if "MarketingDescription" in cabin_class else ''
        return CabinClass(class_of_service=class_of_service, cabin_type=cabin_type, marketing_description=marketing_description)

    def __get_row_info(self, rows):
        row_info = []
        for row in rows:
            row_number = from_json_safe(row, "RowNumber")
            row_facility = self.__get_row_facility_info(ensure_list(from_json_safe(row, "RowFacility"))) if "RowFacility" in row else []
            type_info = self.__get_type_info(from_json_safe(row, "Type"))
            seat = self.__get_seat_info(from_json_safe(row, "Seat")) if from_json_safe(row, "Seat") else []
            row_info.append(RowInfo(row_number=row_number, type_info=type_info, seat_info=seat, row_facility=row_facility))
        return row_info

    def __get_type_info(self, type_info):
        return [TypeInfo(extension=from_json_safe(seat_type, "@extension") if "@extension" in seat_type else seat_type, code=from_json_safe(seat_type, "#text") if "#text" in seat_type else '') for seat_type in ensure_list(type_info)]

    def __get_facility(self, facility_info):
        return [FaciltyInfo(location=from_json_safe(facility, "Location") if "Location" in facility else '', caracteristics=from_json_safe(facility, "Characteristics") if "Characteristics" in facility else '') for facility in facility_info]

    def __get_row_facility_info(self, row_facilty_info):
        row_facilitiies = []
        for row_facility in row_facilty_info:
            location = from_json_safe(row_facility, "Location") if "Location" in row_facility else ''
            facility = self.__get_facility(ensure_list(from_json_safe(row_facility, "Facility"))) if "Facility" in row_facility else []
            row_facilitiies.append(RowFacilityInfo(location=location, facility=facility))
        return row_facilitiies

    def __get_seat_info(self, seat_info):
        seats = []
        for seat in seat_info:
            occupied_ind = from_json_safe(seat, "@occupiedInd")
            inoperative_ind = from_json_safe(seat, "@inoperativeInd")
            premium_ind = from_json_safe(seat, "@premiumInd")
            chargeable_ind = from_json_safe(seat, "@chargeableInd")
            exit_row_ind = from_json_safe(seat, "@exitRowInd")
            restricted_recline_ind = from_json_safe(seat, "@restrictedReclineInd")
            no_infant_ind = from_json_safe(seat, "@noInfantInd")
            number = from_json_safe(seat, "Number")
            occupation = self.__get_occupation_info(ensure_list(from_json_safe(seat, "Occupation")))
            location = self.__get_location_info(ensure_list(from_json_safe(seat, "Location")))
            facilities = self.__get_facilities_info(ensure_list(from_json_safe(seat, "Facilities")))
            offer = self.__get_offer_info(from_json_safe(seat, "Offer")) if from_json_safe(seat, "Offer") else {}
            limitations = self.__get_limitations_info(ensure_list(from_json_safe(seat, "Limitations")))
            bilateral = {"Characteristic": from_json_safe(seat, "Bilateral", "Characteristic") if "Bilateral" in seat else {}}
            seats.append(SeatInfo(occupied_ind=occupied_ind, inoperative_ind=inoperative_ind, premiun_ind=premium_ind, chargeable_ind=chargeable_ind, exit_row_ind=exit_row_ind, restricted_reclined_ind=restricted_recline_ind, no_infant_ind=no_infant_ind, number=number, occupation=occupation, location=location, facilities=facilities, limitations=limitations, offer=offer, bilateral=bilateral))
        return seats

    def __get_occupation_info(self, occupation_info):
        occupations = []
        for occupation in occupation_info:
            detail = from_json_safe(occupation, "Detail")
            extension = from_json_safe(detail, "@extension") if "@extension" in detail else detail
            code = from_json_safe(detail, "#text") if "#text" in detail else ''
            occupations.append(TypeInfo(extension=extension, code=code))
        return occupations

    def __get_facilities_info(self, facilities_info):
        facilities = []
        for facilitie in facilities_info:
            detail = from_json_safe(facilitie, "Detail")
            extension = from_json_safe(detail, "@extension") if "@extension" in detail else detail
            code = from_json_safe(detail, "#text") if "#text" in detail else ''
            facilities.append(TypeInfo(extension=extension, code=code))
        return facilities

    def __get_total_amount(self, total_amount):
        return TotalAmount(currency_code=from_json_safe(total_amount, "@currencyCode") if "@currencyCode" in total_amount else 'USD', text=float(from_json_safe(total_amount, "#text")) if "#text" in total_amount else 0.0)

    def __get_taxe(self, taxe):
        return TotalAmount(currency_code=from_json_safe(taxe, "@currencyCode") if "@currencyCode" in taxe else 'USD', text=float(from_json_safe(taxe, "#text")) if "#text" in taxe else 0.0)

    def __get_taxes(self, taxes):
        taxe = self.__get_taxe(from_json_safe(taxes, "Tax") if "Tax" in taxes else {})
        tax_type_ref = from_json_safe(taxes, "TaxTypeRef") if "TaxTypeRef" in taxes else ''
        return Taxes(tax=taxe, tax_type_ref=tax_type_ref)

    def __get_base_price(self, base_price):
        total_amount = self.__get_total_amount(from_json_safe(base_price, "TotalAmount") if "TotalAmount" in base_price else {})
        taxes = self.__get_taxes(from_json_safe(base_price, "Taxes") if "Taxes" in base_price else {})
        price_type_ref = from_json_safe(base_price, "PriceTypeRef") if "PriceTypeRef" in base_price else ''
        return BasePrice(total_amount=total_amount, taxes=taxes, price_type_ref=price_type_ref)

    def __get_offer_info(self, offer_info):
        entitled_ind = from_json_safe(offer_info, "@entitledInd") if "@entitledInd" in offer_info else ''
        base_price = self.__get_base_price(from_json_safe(offer_info, "BasePrice") if "BasePrice" in offer_info else '')
        return Offer(entitled_ind=entitled_ind, base_price=base_price)

    def __get_limitations_info(self, limitations_info):
        limitations = []
        for limitation in limitations_info:
            detail = from_json_safe(limitation, "Detail")
            extension = from_json_safe(detail, "@extension") if "@extension" in detail else detail
            code = from_json_safe(detail, "#text") if "#text" in detail else ''
            limitations.append(TypeInfo(extension=extension, code=code))
        return limitations

    def __get_location_info(self, location_info):
        locations = []
        for location in location_info:
            detail = from_json_safe(location, "Detail")
            extension = from_json_safe(detail, "@extension") if "@extension" in detail else detail
            code = from_json_safe(detail, "#text") if "#text" in detail else ''
            locations.append(TypeInfo(extension=extension, code=code))
        return locations

    def __get_column_info(self, column_info):
        return [ColumnInfo(column=from_json_safe(column, "Column"), caracteristics=from_json_safe(column, "Characteristics")) for column in column_info]


class UpdatePassengerExtractor(BaseResponseExtractor):

    """Class to extract the send remark from XML response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="PassengerDetailsRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body", "PassengerDetailsRS")
        status = from_json(payload, "ApplicationResults", "@status")
        return {'status': status}


class CloseSessionExtractor(BaseResponseExtractor):
    """
        Will extract response from close session
    """

    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "SessionCloseRS")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        status = from_json(payload, "SessionCloseRS", "@status")
        if status == 'Approved':
            return True
