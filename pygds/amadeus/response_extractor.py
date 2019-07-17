from pygds.core import xmlparser
from pygds.core import helpers
from pygds.amadeus.amadeus_types import AmadeusSessionInfo, GdsResponse


class BaseResponseExtractor(object):
    """
        This is a base class for all response extractor. A helpful class to extract useful info from an XML.
    """
    def __init__(self, xml_content: str):
        """
        constructor for base class
        :param xml_content: The content as XML
        """
        self.xml_content = xml_content
        self.tree = None
        self.parsed = False
        self.session_info = None

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
        if self.session_info is None and not isinstance(self, SessionExtractor):
            self.session_info = SessionExtractor(self.xml_content).extract().session_info
            return GdsResponse(self.session_info, self._extract())
        return GdsResponse(self._extract())

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
        seq, tok, ses, m_id, status = xmlparser.extract_single_elements(
            self.tree, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()",
            "//*[local-name()='SessionId']/text()", "//*[local-name()='RelatesTo']/text()", "//*[local-name()='Session']/@TransactionStatusCode")
        return AmadeusSessionInfo(tok, int(seq), ses, m_id, status)


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

        flights = helpers.get_data_from_json(payload, "flightIndex")
        flights = helpers.ensure_list(flights)
        for rec in recommendations:
            prices = helpers.get_data_from_json(rec, "recPriceInfo", "monetaryDetail")  # [0].amount
            price = helpers.ensure_list(prices)[0]["amount"]
            segmentFlights = helpers.get_data_from_json(rec, "segmentFlightRef")
            segmentFlights = helpers.ensure_list(segmentFlights)
            for seg in segmentFlights:
                reco = {"price": price}
                segs = []
                flightIndexes = helpers.get_data_from_json(seg, "referencingDetail")
                flightIndexes = helpers.ensure_list(flightIndexes)
                flightIndexes = [x["refNumber"] for x in flightIndexes if x["refQualifier"] == 'S']
                for idx, val in enumerate(flightIndexes):
                    legs = []
                    flightDetails = flights[idx]["groupOfFlights"][int(val) - 1]["flightDetails"]
                    flightDetails = helpers.ensure_list(flightDetails)
                    for leg, flight in enumerate(flightDetails):
                        flight_info = helpers.get_data_from_json(flight, "flightInformation")
                        flight_nunber = helpers.get_data_from_json(flight_info, "flightOrtrainNumber")
                        locations = helpers.get_data_from_json(flight_info, "location")
                        locations = helpers.ensure_list(locations)
                        board_airport = locations[0]["locationId"]
                        off_airport = locations[1]["locationId"]
                        dep_date_time = flight_info["productDateTime"]
                        departure_date = dep_date_time["dateOfDeparture"]
                        departure_time = dep_date_time["timeOfDeparture"]
                        comapny_info = flight_info["companyId"]
                        market_company = comapny_info["marketingCarrier"]
                        oper_company = comapny_info["marketingCarrier"]
                        fare_details = helpers.ensure_list(rec["paxFareProduct"])[0]["fareDetails"]
                        helpers.ensure_list(fare_details)
                        product_detail = helpers.ensure_list(fare_details[idx]["groupOfFares"])[leg]["productInformation"]
                        book_class = product_detail["cabinProduct"]["rbd"]
                        fare_basis = product_detail["fareProductDetail"]["fareBasis"]
                        legd = {
                            "fare_basis": fare_basis, "board_airport": board_airport, "off_airport": off_airport,
                            "flight_nunber": flight_nunber, "departure_date": departure_date,
                            "departure_time": departure_time, "marketing_company": market_company,
                            "operator_company": oper_company, "book_class": book_class
                        }
                        legs.append(legd)
                    segs.append(legs)
                reco["segments"] = segs
                recs.append(reco)
        return recs


class CommandReplyExtractor(BaseResponseExtractor):
    """
        Class command reply from XML Response
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content)
        self.parsed = True

    def _extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Command_CrypticReply")
        return helpers.get_data_from_json(payload, "longTextString", "textStringDetails")

