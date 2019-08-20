from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core import xmlparser
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml
import logging
from pygds.core.sessions import SessionInfo
from pygds.core.price import AirItineraryPricingInfo, SearchPriceInfos
from pygds.core.ticket import TicketReply
import re

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
        return GdsResponse(None, self._extract(), None)
        


    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")



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
        for air_itinerary_pricing_inf in air_itinerary_pricing:
            # itin_totalfare = from_json(payload, "PriceQuote", "PricedItinerary", "AirItineraryPricingInfo", "ItinTotalFare")
            # base_fare = from_json(itin_totalfare, "EquivFare", "@Amount") if "EquivFare" in itin_totalfare else from_json(itin_totalfare, "BaseFare", "@Amount")
            # taxes = from_json(itin_totalfare, "Taxes", "@TotalAmount")
            # total_fare = from_json(itin_totalfare, "TotalFare", "@Amount")
            # currency_code = from_json(itin_totalfare, "TotalFare", "@CurrencyCode")
            # air_itinerary_pricing_info = AirItineraryPricingInfo()
            # air_itinerary_pricing_info.base_fare = base_fare
            # air_itinerary_pricing_info.taxes = taxes
            # air_itinerary_pricing_info.total_fare = total_fare
            # air_itinerary_pricing_info.currency_code = currency_code

            # search_price_infos = SearchPriceInfos()
            # search_price_infos.status = status
            # search_price_infos.air_itinerary_pricing_info = air_itinerary_pricing_info
            passengers = self._get_passengers(air_itinerary_pricing_inf)
            return passengers

    def _get_passengers(self, air_itinerary_pricing):
        passenger_infos = []

        for i in from_json(air_itinerary_pricing, "PassengerTypeQuantity", "@Quantity"):
            pax_info = {
                "ItinTotalFare" : from_json(air_itinerary_pricing, "ItinTotalFare"),
                "PassengerType" : from_json(air_itinerary_pricing, "PassengerTypeQuantity", "@Code"),
                "ChargeAmount" : from_json(air_itinerary_pricing, "ItinTotalFare",  "TotalFare", "@Amount"),
                "TourCode" : self._get_tour_code(air_itinerary_pricing),
                "TicketDesignator" : self._get_get_ticket_designator(air_itinerary_pricing),
                "CommissionPercentage" : self._get_commission_percent(air_itinerary_pricing)
            }
            passenger_infos.append(pax_info)
        
        return passenger_infos
    
    
    def _get_tour_code(self, air_itinerary_pricing):
        result = None
        if "Endorsements" in from_json(air_itinerary_pricing, "ItinTotalFare")  and from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text"):
            text = from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text")
            if 'TC' in text:
                text = re.findall("TC ([0-9A-Z]+)", str)[0]
                result = text
        return result


    def _get_get_ticket_designator(self, air_itinerary_pricing):
        result = None
        if "Endorsements" in from_json(air_itinerary_pricing,"ItinTotalFare") and from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text"):
            text = from_json(air_itinerary_pricing, "ItinTotalFare", "Endorsements", "Text")
            if 'TD' in text:
                text = re.findall("TD ([0-9A-Z]+)", str)[0]
                result = text
        return result


    def _get_commission_percent(self, air_itinerary_pricing):
        result = 0

        if "PTC_FareBreakdown" in air_itinerary_pricing and isinstance(from_json(air_itinerary_pricing, "PTC_FareBreakdown"), list) and len(from_json(air_itinerary_pricing, "PTC_FareBreakdown")) > 0 :
            fare_breakdown = from_json(air_itinerary_pricing, "PTC_FareBreakdown")
            text = from_json(fare_breakdown[0], "FareBasis", "@Code")
            if 'CM' in text:
                text = re.findall("CM([0-9]+)", text)[0]
                result = text
        return result



class IssueTicketExtractor(BaseResponseExtractor):
    """
        Class to extract issue ticket information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="Fault")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Body")
        response_data = from_json_safe(payload, "AirTicketRS")
        application_result_data = from_json_safe(response_data, "ApplicationResults")
        status = from_json_safe(application_result_data ,"status")
        success_data = from_json_safe(application_result_data, "Success")
        error_data = from_json_safe(application_result_data, "Error")
        warning_data = from_json_safe(application_result_data, "Warning")
        text_data = from_json_safe(response_data, "Text")
        error_data = from_json_safe(payload, "Fault")
        if error_data:
            fault_code = from_json_safe(error_data, "faultcode")
            fault_string = from_json_safe(error_data, "faultstring")
            details = from_json_safe(error_data, "detail")
            stack_trace = from_json_safe(details, "StackTrace")
            application_results = from_json_safe(details, "ApplicationResults")
            status_error = from_json_safe(application_results, "status")
            error_application_results = from_json_safe(application_results, "Error")
            time_stamp = from_json_safe(error_application_results, "timeStamp")
            error_type = from_json_safe(error_application_results, "type")
            system_specific_results = from_json_safe(error_application_results, "SystemSpecificResults")
            message = from_json_safe(system_specific_results , "Message")
            message_text = from_json_safe(message, "text")
            short = from_json_safe(system_specific_results, "ShortText")
            short_text = from_json_safe(short, "text")
        else:
            fault_code, fault_string, stack_trace, status_error, time_stamp, error_type, message_text, short_text = (None, None, None, None, None, None, None, None)
        return TicketReply(status, status_error, fault_code, fault_string, message_text, text_data, error_data, warning_data, success_data)