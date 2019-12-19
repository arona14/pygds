import fnc
from typing import List
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor, extract_amount
from pygds.core.types import PassengerBasicInfo
from pygds.core.price import TSTInfo, SearchPriceInfos, FareAmount, TaxInformation, AirItineraryPricingInfo, FareBreakdown
from pygds.core.helpers import get_data_from_xml as from_xml, ensure_list


class CreateTstResponseExtractor(BaseResponseExtractor):
    """
    Wil extract response of create TST from price
    """

    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "Ticket_CreateTSTFromPricingReply")

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Ticket_CreateTSTFromPricingReply")
        pnr = None
        status = None
        for reservation in ensure_list(fnc.get("pnrLocatorData.reservation", payload)):
            if not pnr:
                pnr = fnc.get("controlNumber", reservation)
            if fnc.get("controlType", reservation) == "5":
                status = fnc.get("controlNumber", reservation)
            if pnr and status:
                break
        for tst_data in ensure_list(fnc.get("tstList", payload, default=[])):
            tst_ref = fnc.get("tstReference.uniqueReference", tst_data)
            all_passengers = []
            all_segments = []
            for p in ensure_list(
                fnc.get("paxInformation.refDetails", tst_data, default=[])
            ):
                if fnc.get("refQualifier", p) != "S":
                    passenger_type = fnc.get("refQualifier", p)
                    passenger_ref = fnc.get("refNumber", p)
                    all_passengers.append(PassengerBasicInfo(passenger_ref, passenger_type))
                else:
                    all_segments.append(fnc.get("refNumber", p))

            tst_info = TSTInfo(status=status, pnr=pnr, tst_ref=tst_ref, passengers=all_passengers, segments=all_segments)
            return tst_info
        return None


class DisplayTSTExtractor(BaseResponseExtractor):
    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "Ticket_DisplayTSTReply")

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Ticket_DisplayTSTReply")

        for fare in ensure_list(fnc.get("fareList", payload)):
            search_price_infos = SearchPriceInfos()
            search_price_infos.status = fnc.get("statusInformation.firstStatusDetails.tstFlag", fare)
            search_price_infos.air_itinerary_pricing_info = self.get_air_itinerary_pricing_info(fare)
            return search_price_infos
        return None

    def get_air_itinerary_pricing_info(self, fare: dict = {}):
        validating_carier = fnc.get(
            "validatingCarrier.carrierInformation.carrierCode", fare
        )
        base_fare, total_fare, _ = self._tst_amounts(
            fnc.get("fareDataInformation.fareDataSupInformation", fare)
        )
        total_taxes, _ = self._tst_taxes(
            fnc.get("taxInformation", fare)
        )

        currency_code = base_fare.currency

        all_pax_ref = ensure_list(
            fnc.get("paxSegReference.refDetails", fare, default=[])
        )
        all_passengers = [
            fnc.get("refQualifier", pax_ref) for pax_ref in all_pax_ref if fnc.get("refQualifier", pax_ref) != "S"
        ]

        passenger_type = all_passengers[0] if all_passengers else None
        passenger_quantity = len(all_passengers)
        bagage_provisions = []

        fare_basis_code = None
        ticket_designator = None
        class_of_service = None
        tour_code = ""
        commission_percentage = ""
        fare_type = None
        amount = None

        qualifier = fnc.get("fareDataInformation.fareDataMainInformation.fareDataQualifier", fare)
        if qualifier == "H":
            fare_type = "NET"
            amount = fnc.get("fareDataInformation.fareDataMainInformation.fareAmount", fare)
        if qualifier == "PU":
            fare_type = "PUB"
            amount = fnc.get("fareDataInformation.fareDataMainInformation.fareAmount", fare)

        all_fare_break_down = []
        for segment_information in ensure_list(fnc.get("segmentInformation", fare, default=[])):
            bag = fnc.get("bagAllowanceInformation.bagAllowanceDetails.baggageQuantity", segment_information)
            if not class_of_service:
                class_of_service = fnc.get("segDetails.segmentDetail.classOfService", segment_information)
            if bag:
                bagage_provisions.append(
                    bag
                )
            for fare_qualifier in ensure_list(fnc.get("fareQualifier", segment_information, default=[])):
                if not ticket_designator:
                    ticket_designator = fnc.get("fareBasisDetails.ticketDesignator", fare_qualifier)
                if not fare_basis_code:
                    fare_basis_code = fnc.get("fareBasisDetails.fareBasisCode", fare_qualifier)

            fare_break_down = FareBreakdown()
            fare_break_down.cabin = class_of_service
            fare_break_down.fare_amount = amount if amount else base_fare.amount
            fare_break_down.fare_passenger_type = passenger_type
            fare_break_down.free_baggage = bag
            fare_break_down.fare_type = fare_type
            fare_break_down.fare_basis_code = fare_basis_code
            fare_break_down.filing_carrier = ""
            all_fare_break_down.append(fare_break_down)

        air_itinerary_pricing_infos = AirItineraryPricingInfo()
        air_itinerary_pricing_infos.passenger_type = passenger_type
        air_itinerary_pricing_infos.baggage_provisions = bagage_provisions
        air_itinerary_pricing_infos.passenger_quantity = passenger_quantity
        air_itinerary_pricing_infos.ticket_designator = ticket_designator
        air_itinerary_pricing_infos.commission_percentage = commission_percentage
        air_itinerary_pricing_infos.base_fare = base_fare.amount
        air_itinerary_pricing_infos.total_fare = total_fare.amount
        air_itinerary_pricing_infos.charge_amount = base_fare.amount
        air_itinerary_pricing_infos.taxes = total_taxes.amount
        air_itinerary_pricing_infos.tour_code = tour_code
        air_itinerary_pricing_infos.fare_break_down = all_fare_break_down
        air_itinerary_pricing_infos.valiating_carrier = validating_carier
        air_itinerary_pricing_infos.currency_code = currency_code
        return air_itinerary_pricing_infos

    def _tst_amounts(self, fare_data_main_informations: List):
        amounts = []
        base_fare = None
        total_fare = None
        for am in ensure_list(fare_data_main_informations):
            am = extract_amount(am, "fareDataQualifier", "fareAmount", "fareCurrency")
            if am.qualifier == "B" and not base_fare:
                base_fare = am
            if am.qualifier == "E":
                base_fare = am
            elif am.qualifier == "TFT":
                total_fare = am
            amounts.append(am)
        return base_fare, total_fare, amounts

    def _tst_taxes(self, tax_informations: List):
        total_taxes = 0.0
        total_taxes_currency = None
        taxes = []
        for tax_info in ensure_list(tax_informations):
            tax: TaxInformation = TaxInformation()
            tax.tax_type = fnc.get("taxDetails.taxType.isoCountry", tax_info)
            tax.tax_nature = fnc.get("taxDetails.taxNature", tax_info)
            amount_details = fnc.get("amountDetails.fareDataMainInformation", tax_info)
            am = extract_amount(
                amount_details,
                "fareDataQualifier", "fareAmount", "fareCurrency")
            tax.tax_amount = am
            if not total_taxes_currency:
                total_taxes_currency = am.currency
            if am.currency == total_taxes_currency:  # avoid summing amounts on different currencies
                total_taxes += float(am.amount)
            taxes.append(tax)
        total_taxes = FareAmount(None, str(round(total_taxes, 2)), total_taxes_currency)
        return total_taxes, taxes
