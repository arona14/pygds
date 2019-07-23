from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core import xmlparser
from pygds.core import helpers
from pygds.core.sessions import SessionInfo


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
            A private method that does the work of extracting useful data.
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
        return SessionInfo(tok, int(seq), ses, m_id, status != "InSeries")


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

class FormOfPaymentExtractor(BaseResponseExtractor):
    """
        Class to extract form of payment information from XML response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content)

    def _extract(self):
        return None


class GetPnrResponseExtractor(BaseResponseExtractor):
    """
        A class to extract Reservation from response of retrieve PNR.
    """
    def __init__(self, xml_content: str):
        super().__init__(xml_content)
        self.parsed = True

    def _extract(self):
        payload = helpers.get_data_from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")
        self.payload = payload
        return {
            'itineraries': self._segments(),
            'passengers': self._passengers(),
            'form_of_payments': self._form_of_payments(),
            'price_quotes': self._price_quotes(),
            'ticketing_info': self._ticketing_info()
        }

    def _segments(self):
        segments_list = []
        for data in self.payload["originDestinationDetails"]["itineraryInfo"]:
            segment_data = {}
            dep_date = data["travelProduct"]["product"]["depDate"]
            dep_time = data["travelProduct"]["product"]["depTime"]

            arr_date = data["travelProduct"]["product"]["arrDate"]
            arr_time = data["travelProduct"]["product"]["arrTime"]

            segment_data["departure_airport"] = data["travelProduct"]["boardpointDetail"]["cityCode"]
            segment_data["arrival_airport"] = data["travelProduct"]["offpointDetail"]["cityCode"]
            segment_data["departure_dateTime"] = helpers.reformat_date(dep_date + dep_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            segment_data["arrival_date_time"] = helpers.reformat_date(arr_date + arr_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            segment_data['equipment_type'] = data["flightDetail"]["productDetails"]["equipment"]
            segment_data['class_of_service'] = data["travelProduct"]["productDetails"]["classOfService"]

            segments_list.append(segment_data)
        return segments_list

    def _passengers(self):
        passengers_list = []
        for traveller in helpers.ensure_list(helpers.get_data_from_json(self.payload, "travellerInfo")):
            passenger_data = {}
            data = helpers.get_data_from_json(traveller, "passengerData")
            traveller_info = helpers.get_data_from_json(data, "travellerInformation")
            trvl = helpers.get_data_from_json(traveller_info, "traveller")
            psngr = helpers.get_data_from_json(traveller_info, "passenger")
            date_of_birth_tag = helpers.get_data_from_json(data, "dateOfBirth", "dateAndTimeDetails")

            date = helpers.get_data_from_json(date_of_birth_tag, "date")
            date_of_birth = helpers.reformat_date(date, "%d%m%Y", "%Y-%m-%d")
            passenger_data['surname'] = helpers.get_data_from_json(trvl, "surname")
            passenger_data['quantity'] = helpers.get_data_from_json(trvl, "quantity")
            passenger_data['firstname'] = helpers.get_data_from_json(psngr, "firstName")
            passenger_data['type'] = helpers.get_data_from_json(psngr, "type")
            passenger_data['qualifier'] = helpers.get_data_from_json(date_of_birth_tag, "qualifier")
            passenger_data['date_of_birth'] = date_of_birth
            passengers_list.append(passenger_data)
        return passengers_list

    def _pnr_info(self):
        pnr_infos = []
        for data in self.payload["pnrHeader"]["reservationInfo"]["reservation"]:
            reservation_info = {
                'compagny_id': data["companyId"],
                'control_number': data["reservationInfo"]["reservation"]["controlNumber"]
            }

            res_date = data["reservationInfo"]["reservation"]["date"]
            res_time = data["reservationInfo"]["reservation"]["time"]
            date_time = helpers.reformat_date(res_date + res_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            reservation_info['date_time'] = date_time
            pnr_infos.append(reservation_info)
        return pnr_infos

    def _price_quotes(self):
        price_quotes = []
        pqs = helpers.get_data_from_json(self.payload, "pricingRecordGroup", "productPricingQuotationRecord")
        pqs = helpers.ensure_list(pqs)
        for data in pqs:
            price_quotes_details = {
                'pricing_record_id': data['pricingRecordId'],
                'passenger_tattoos': data['passengerTattoos'],
                'total_fare': data['documentDetailsGroup']['totalFare']
            }
            price_quotes.append(price_quotes_details)
        return price_quotes

    def _form_of_payments(self):
        return None

    def _ticketing_info(self):
        return None
