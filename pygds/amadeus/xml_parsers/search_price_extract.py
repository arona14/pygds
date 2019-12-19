from pygds.core.helpers import get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml
from pygds.core.price import AirItineraryPricingInfo, FareBreakdown, SearchPriceInfos
import fnc
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor
import re


class PricePNRExtractor(BaseResponseExtractor):
    """
    this class is to extract price information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="Fare_PricePNRWithBookingClassReply")
        self.parsed = True

    def default_value(self):
        return []

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Fare_PricePNRWithBookingClassReply")
        fare_list = ensure_list(from_json_safe(payload, "fareList"))
        air_itinerary_pricing_list = []
        list_fare_break_down = []
        search_price = None
        commission_percentage = 0
        tour_code = ""
        ticket_designator = ""
        for fare in fare_list:
            air_itinerary_pricing_info = AirItineraryPricingInfo()
            commission_info = self._get_commission_info(fare)
            if len(commission_info) > 3 and "CM" in commission_info:
                commission_percentage = commission_info[2:]
            total_fare, currency_code = self._get_total_fare_and_currency_code(fare)
            air_itinerary_pricing_info.base_fare = self._get_equive_fare(fare) or self._get_base_fare(fare)
            air_itinerary_pricing_info.taxes = round(sum(self._get_taxes(fare)), 2)
            air_itinerary_pricing_info.total_fare = total_fare
            air_itinerary_pricing_info.currency_code = currency_code
            tst_reference = fnc.get("fareReference.referenceType", fare)
            if tst_reference and tst_reference.upper() == "TST":
                air_itinerary_pricing_info.tst_ref = fnc.get("fareReference.uniqueReference", fare)
            air_itinerary_pricing_info.passenger_type = self._get_pax_type(fare)
            air_itinerary_pricing_info.passenger_quantity = self._get_pax_quantity(fare)
            air_itinerary_pricing_info.charge_amount = total_fare
            text = self._get_tour_code_and_ticket_designator(fare)
            if "TC" in text:
                tour_code = re.findall("TC" + " ([0-9A-Z]+)", text)
            if "TD" in text:
                ticket_designator = re.findall("TD" + " ([0-9A-Z]+)", text)
            if len(tour_code) > 0:
                air_itinerary_pricing_info.tour_code = tour_code[0]
            air_itinerary_pricing_info.commission_percentage = commission_percentage
            if len(ticket_designator) > 0:
                air_itinerary_pricing_info.ticket_designator = ticket_designator[0]
            air_itinerary_pricing_info.valiating_carrier = fnc.get("validatingCarrier.carrierInformation.carrierCode", fare)
            fare_break_down = FareBreakdown()
            for seg_infos in ensure_list(fnc.get("segmentInformation", fare, default=[])):
                fare_break_down.fare_basic_code = fnc.get("fareQualifier.fareBasisDetails.fareBasisCode", seg_infos)
                fare_break_down.cabin = fnc.get("cabinGroup.cabinSegment.bookingClassDetails.option", seg_infos)
                fare_break_down.fare_passenger_type = self._get_pax_type(fare)
                fare_break_down.fare_amount = ""
                fare_break_down.fare_type = ""
                fare_break_down.filing_carrier = ""
                fare_break_down.free_baggage = fnc.get("bagAllowanceInformation.bagAllowanceDetails", seg_infos)
                list_fare_break_down.append(fare_break_down)
            air_itinerary_pricing_info.fare_break_down = list_fare_break_down
            air_itinerary_pricing_list.append(air_itinerary_pricing_info)
            search_price = SearchPriceInfos()
            search_price.status = ""
            search_price.air_itinerary_pricing_info = air_itinerary_pricing_list
        return search_price

    def _get_tour_code_and_ticket_designator(self, fare):
        """
        This method return the tour code
        :param fare: a dictionary containing fare info
        return: tour code
        """
        other_price_infos = ensure_list(fnc.get("otherPricingInfo", fare, default=[]))
        for other_price_info in other_price_infos:
            for attribut_details in fnc.get("attributeDetails", other_price_info):
                if fnc.get("attributeType", attribut_details) == "END":
                    return fnc.get("attributeDescription", attribut_details)
        return None

    def _get_commission_info(self, fare):
        """
        This method return the ticket designator
        :param fare: a dictionnary containing the fare info
        :return: ticket designator
        """
        segment_infos = ensure_list(fnc.get("segmentInformation", fare, default=[]))
        for segment_info in segment_infos:
            commission_info = fnc.get("fareQualifier.fareBasisDetails.ticketDesignator", segment_info)
        return commission_info

    def _get_pax_type(self, fare):
        """
        look for passenger references
        :param fare: a dictionary containing fare info
        :return: List[str]
        """
        for pax_ref in ensure_list(from_json_safe(fare, "paxSegReference", "refDetails")):
            if fnc.get("refQualifier", pax_ref) == 'PA':
                pax_type = "ADT"
            elif fnc.get("refQualifier", pax_ref) == "PI":
                pax_type = "INF"
        return pax_type

    def _get_pax_quantity(self, fare):
        """
        this return the quantity of passengers
        :param fare: a dictionary containing fare info
        :return: List[str]
        """
        quantity = 0
        for pax_ref in ensure_list(from_json_safe(fare, "paxSegReference", "refDetails")):
            quantity += 1
        return quantity

    def _get_equive_fare(self, fare):
        """
        this method return the equive_fare
        :param fare: a dictionnary containing fare info
        :return : equive_fare
        """
        fare_d_information = fnc.get("fareDataInformation", fare)

        for f_d_m_i in ensure_list(fnc.get("fareDataSupInformation", fare_d_information, default=[])):
            if fnc.get("fareDataQualifier", f_d_m_i) == "E":
                return fnc.get("fareAmount", f_d_m_i)
        return None

    def _get_base_fare(self, fare):
        """
        this method return the equive_fare
        :param fare: a dictionnary containing fare info
        :return : equive_fare
        """
        fare_d_information = fnc.get("fareDataInformation", fare)
        for f_d_m_i in ensure_list(fnc.get("fareDataSupInformation", fare_d_information, default=[])):
            if fnc.get("fareDataQualifier", f_d_m_i) == "B":
                return fnc.get("fareAmount", f_d_m_i)
        return None

    def _get_total_fare_and_currency_code(self, fare):
        """
        this method return the equive_fare
        :param fare: a dictionnary containing fare info
        :return : equive_fare
        """
        fare_d_information = fnc.get("fareDataInformation", fare)
        for f_d_m_i in ensure_list(fnc.get("fareDataSupInformation", fare_d_information, default=[])):
            if fnc.get("fareDataQualifier", f_d_m_i) not in ["E", "B"]:
                return fnc.get("fareAmount", f_d_m_i), fnc.get("fareCurrency", f_d_m_i)

        return None

    def _get_taxes(self, fare):

        """
        look for taxes
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        taxes = []
        for tax_infos in ensure_list(fnc.get("taxInformation", fare, default=[])):
            tax = float(fnc.get("amountDetails.fareDataMainInformation.fareAmount", tax_infos))
            taxes.append(tax)

        return taxes
