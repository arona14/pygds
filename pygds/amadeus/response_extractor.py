# from pygds.core.types import FlightSegment, FlightPointDetails
from ..core import xmlparser
from ..core import helpers
from .amadeus_types import AmadeusSessionInfo


class BaseResponseExtractor(object):
    """
        This is a base class for all response extractor. A helpful class to extract useful info from an XML.
    """
    def __init__(self, xml_content: str):
        self.xml_content = xml_content
        self.tree = None
        self.parsed = False

    def parse(self):
        """
            If not already done, it parses the XML content to JSON and save it.
        """
        if not self.parsed:
            print(".parse called")
            self.tree = xmlparser.parse_xml(self.xml_content)
            self.parsed = True

    def extract(self):
        """
            The public method to call when extracting useful data.
        """
        print(".extract called")
        self.parse()
        return self._extract()

    def _extract(self):
        """
            A private method that does the work of extracting usefull data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class ErrorExtractor(BaseResponseExtractor):
    """
        Extractor for error
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        return xmlparser.extract_single_elements(self.tree, "//faultcode/text()", "//faultstring/text()")


class SessionExtractor(BaseResponseExtractor):
    """
        Class to extract session information from XML response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        print("SessionExtractor._extract called")
        seq, tok, ses, mes_id = xmlparser.extract_single_elements(self.tree, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()", "//*[local-name()='SessionId']/text()", "//*[local-name()='RelatesTo']/text()")
        return AmadeusSessionInfo(tok, int(seq), ses, mes_id)


class PriceSearchExtractor(BaseResponseExtractor):
    """
        Class to extract price search information from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content)
        self.parsed = True

    def _extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Fare_MasterPricerTravelBoardSearchReply")
        recommendations = helpers.get_data_from_json(payload, "recommendation")
        recommendations = helpers.ensure_list(recommendations)
        recs = []
        currency = helpers.get_data_from_json(payload, "conversionRate", "conversionRateDetail", "currency")

        flights = helpers.get_data_from_json(payload, "flightIndex")
        flights = helpers.ensure_list(flights)
        for rec in recommendations:
            prices = helpers.get_data_from_json(rec, "recPriceInfo", "monetaryDetail")  # [0].amount
            price = helpers.ensure_list(prices)[0]["amount"]
            segment_flights = helpers.get_data_from_json(rec, "segmentFlightRef")
            segment_flights = helpers.ensure_list(segment_flights)
            for seg in segment_flights:
                reco = {"price": price, "currency": currency}
                itineraries = []
                flight_indexes = helpers.get_data_from_json(seg, "referencingDetail")
                flight_indexes = helpers.ensure_list(flight_indexes)
                flight_indexes = [x["refNumber"] for x in flight_indexes if x["refQualifier"] == 'S']
                for idx, val in enumerate(flight_indexes):
                    segments = []
                    flight_details = flights[idx]["groupOfFlights"][int(val) - 1]["flightDetails"]
                    flight_details = helpers.ensure_list(flight_details)
                    for leg, flight in enumerate(flight_details):
                        flight_info = helpers.get_data_from_json(flight, "flightInformation")
                        flight_number = helpers.get_data_from_json(flight_info, "flightOrtrainNumber")
                        locations = helpers.get_data_from_json(flight_info, "location")
                        locations = helpers.ensure_list(locations)
                        board_airport = locations[0]["locationId"]
                        off_airport = locations[1]["locationId"]
                        dep_date_time = flight_info["productDateTime"]
                        departure_date = dep_date_time["dateOfDeparture"]
                        departure_time = dep_date_time["timeOfDeparture"]
                        arrival_date = dep_date_time["dateOfArrival"]
                        arrival_time = dep_date_time["timeOfArrival"]
                        company_info = flight_info["companyId"]
                        market_company = company_info["marketingCarrier"]
                        oper_company = company_info["marketingCarrier"]
                        fare_details = helpers.ensure_list(rec["paxFareProduct"])[0]["fareDetails"]
                        fare_details = helpers.ensure_list(fare_details)
                        product_detail = helpers.ensure_list(fare_details[idx]["groupOfFares"])[leg]["productInformation"]
                        book_class = product_detail["cabinProduct"]["rbd"]
                        fare_basis = product_detail["fareProductDetail"]["fareBasis"]
                        # departure = FlightPointDetails(departure_date, departure_time, 0, "", board_airport, "", "")
                        # arrival = FlightPointDetails(arrival_date, arrival_time, 0, "", off_airport, "", "")
                        # segment = FlightSegment(0, departure, arrival, market_company, flight_number, book_class, "")
                        segment = {
                            "fare_basis": fare_basis, "board_airport": board_airport, "off_airport": off_airport,
                            "flight_number": flight_number, "departure_date": departure_date,
                            "departure_time": departure_time, "arrival_date": arrival_date, "arrival_time": arrival_time
                            , "marketing_company": market_company, "operator_company": oper_company,
                            "book_class": book_class
                        }
                        segments.append(segment)
                    itineraries.append(segments)
                reco["itineraries"] = itineraries
                recs.append(reco)
        return recs


class AddMultiElementExtractor(BaseResponseExtractor):
    def __init__(self, xml_content: str):
        super().__init__(xml_content)
        self.parsed = True

    def _extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")
        pnr = helpers.get_data_from_json(payload, "pnrHeader", "reservationInfo", "reservation")  # , "controlNumber")
        pnr_data = {"pnr_number": pnr}
        travellers_info = helpers.get_data_from_json(payload, "travellerInfo")
        passengers = []
        travellers_info = helpers.ensure_list(travellers_info)
        for idx, pax in enumerate(travellers_info):
            info = helpers.get_data_from_json(pax, "passengerData", "travellerInformation")
            surname = helpers.get_data_from_json(info, "traveller", "surname")
            name = helpers.get_data_from_json(info, "passenger", "firstName")
            passenge_type = helpers.get_data_from_json(info, "passenger", "type")
            date_of_birth = ""  # helpers.get_data_from_json(pax, "passengerData", "dateOfBirth", "dateAndTimeDetails", "date")
            passengers.append({"surname": surname, "name": name, "type": passenge_type, "date_of_birth": date_of_birth})
        pnr_data["passengers"] = passengers

        itineraries_info = helpers.get_data_from_json(payload, "originDestinationDetails", "itineraryInfo")
        itineraries_info = helpers.ensure_list(itineraries_info)
        segments = []
        for idx, seg in enumerate(itineraries_info):
            travel_details = helpers.get_data_from_json(seg, "travelProduct")
            from_city = helpers.get_data_from_json(travel_details, "boardpointDetail", "cityCode")
            to_city = helpers.get_data_from_json(travel_details, "offpointDetail", "cityCode")
            company = helpers.get_data_from_json(travel_details, "companyDetail", "identification")
            product = helpers.get_data_from_json(travel_details, "product")
            dep_date = helpers.get_data_from_json(product, "depDate")
            dep_time = helpers.get_data_from_json(product, "depTime")
            arr_date = helpers.get_data_from_json(product, "arrDate")
            arr_time = helpers.get_data_from_json(product, "arrTime")

            fligth_number = helpers.get_data_from_json(travel_details, "productDetails", "identification")
            segments.append({"from_city": from_city, "to_city": to_city, "company": company, "dep_date": dep_date, "dep_time": dep_time, "arr_date": arr_date, "arr_time": arr_time, "fligth_number": fligth_number})
        pnr_data["segments"] = segments
        return pnr_data


class PricePNRExtractor(BaseResponseExtractor):
    def __init__(self, xml_content: str):
        super().__init__(xml_content)
        self.parsed = True

    def _extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Fare_PricePNRWithBookingClassReply")
        fare_list = helpers.get_data_from_json(payload, "fareList")
        fare_list = helpers.ensure_list(fare_list)
        tst_references = []
        for idx, fare in enumerate(fare_list):
            ref = fare["fareReference"]
            ref_type = ref["referenceType"]
            if ref_type.upper() == "TST":
                tst_references.append(ref["uniqueReference"])
        return tst_references
