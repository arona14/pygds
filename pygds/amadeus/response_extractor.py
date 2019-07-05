from ..core import xmlparser
from ..core import helpers
from .amadeus_types import AmadeusSessionInfo


class BaseResponseExtractor(object):
    def __init__(self, xml_content: str):
        self.xml_content = xml_content
        self.tree = None
        self.parsed = False

    def parse(self):
        if not self.parsed:
            print(".parse called")
            self.tree = xmlparser.parse_xml(self.xml_content)
            self.parsed = True

    def extract(self):
        print(".extract called")
        self.parse()
        return self._extract()

    def _extract(self):
        raise NotImplementedError("Sub class must implement '_extract' method")


class ErrorExtractor(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        print("ErrorExtractor._extract called")
        return xmlparser.extract_single_elements(self.tree, "//faultcode/text()", "//faultstring/text()")


class SessionExtractor(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        print("SessionExtractor._extract called")
        seq, tok, ses = xmlparser.extract_single_elements(self.tree, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()", "//*[local-name()='SessionId']/text()")
        return AmadeusSessionInfo(tok, seq, ses)


class PriceSearchExtractor(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        print("PriceSearchExtractor._extract called")
        response = []
        # recommendations = xmlparser.extract_list_elements(self.tree, "//recommendation")
        # for recommendation in recommendations:
        #     id, = xmlparser.extract_single_elements(recommendation, "//itemNumber/itemNumberId/number/text()")
        #     response.append(id)
        id, = xmlparser.extract_list_elements(self.tree, "//itemNumber/itemNumberId/number/text()")
        response.append(id)
        return response

    def extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Fare_MasterPricerTravelBoardSearchReply")
        recommendations = helpers.get_data_from_json(payload, "recommendation")
        recommendations = helpers.ensure_list(recommendations)
        recs = []

        flights = helpers.get_data_from_json(payload, "flightIndex")
        flights = helpers.ensure_list(flights)
        print(f"number of recommendations : {len(recommendations)}")
        for rec in recommendations:
            prices = helpers.get_data_from_json(rec, "recPriceInfo", "monetaryDetail")  # [0].amount
            price = helpers.ensure_list(prices)[0]["amount"]
            segmentFlights = helpers.get_data_from_json(rec, "segmentFlightRef")
            segmentFlights = helpers.ensure_list(segmentFlights)
            # print(f"> Number of segments: {len(segmentFlights)}")
            for seg in segmentFlights:
                reco = {"price": price}
                segs = []
                flightIndexes = helpers.get_data_from_json(seg, "referencingDetail")
                flightIndexes = helpers.ensure_list(flightIndexes)
                # print(f">> flight indexes objects: {flightIndexes}")
                flightIndexes = [x["refNumber"] for x in flightIndexes if x["refQualifier"] == 'S']
                # print(f">> flight indexes: {flightIndexes}")
                for idx, val in enumerate(flightIndexes):
                    segment = idx + 1
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
