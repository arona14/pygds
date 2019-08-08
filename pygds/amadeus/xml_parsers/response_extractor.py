from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core import xmlparser
import re
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml, reformat_date
from pygds.core.price import Fare, FareAmount, TaxInformation, WarningInformation, FareComponent, CouponDetails, \
    SegmentInformation, ValidityInformation, TstInformation
from pygds.core.sessions import SessionInfo
import logging

from pygds.core.ticket import TicketReply

from pygds.core.types import TicketingInfo, FlightSegment, Remarks, FlightAirlineDetails, FlightPointDetails, \
    FormOfPayment, PnrInfo, Passenger


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
        if self.parse_session and self.session_info is None:
            self.session_info = SessionExtractor(self.xml_content).extract().session_info
        if self.parse_app_error and self.app_error is None:
            self.app_error = AppErrorExtractor(self.xml_content, self.main_tag).extract().application_error
        return GdsResponse(self.session_info, self.default_value() if self.app_error else self._extract(),
                           self.app_error)

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
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", self.main_tag)
        app_error_data = from_json_safe(payload, "applicationError")
        if not app_error_data:
            return None
        details = from_json_safe(app_error_data, "errorOrWarningCodeDetails", "errorDetails")
        error_code = from_json_safe(details, "errorCode")
        error_category = from_json_safe(details, "errorCategory")
        error_owner = from_json_safe(details, "errorCodeOwner")
        description = from_json_safe(app_error_data, "errorWarningDescription", "freeText")
        return ApplicationError(error_code, error_category, error_owner, description)


class SessionExtractor(BaseResponseExtractor):
    """
        Class to extract session information from XML response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, False, False)

    def extract(self):
        response = super().extract()
        response.session_info = response.payload
        return response

    def _extract(self):
        seq, tok, ses, m_id, status = xmlparser.extract_single_elements(
            self.tree, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()",
            "//*[local-name()='SessionId']/text()", "//*[local-name()='RelatesTo']/text()",
            "//*[local-name()='Session']/@TransactionStatusCode")
        return SessionInfo(tok, int(seq), ses, m_id, status != "InSeries")


class PriceSearchExtractor(BaseResponseExtractor):
    """
        Class to extract price search information from XML Response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="Fare_MasterPricerTravelBoardSearchReply")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body",
                           "Fare_MasterPricerTravelBoardSearchReply")
        recommendations = from_json(payload, "recommendation")
        recommendations = ensure_list(recommendations)
        recs = []
        currency = from_json(payload, "conversionRate", "conversionRateDetail", "currency")

        flights = from_json(payload, "flightIndex")
        flights = ensure_list(flights)
        for rec in recommendations:
            prices = from_json(rec, "recPriceInfo", "monetaryDetail")  # [0].amount
            price = ensure_list(prices)[0]["amount"]
            segment_flights = from_json(rec, "segmentFlightRef")
            segment_flights = ensure_list(segment_flights)
            for seg in segment_flights:
                reco = {"price": price, "currency": currency}
                itineraries = []
                flight_indexes = from_json(seg, "referencingDetail")
                flight_indexes = ensure_list(flight_indexes)
                flight_indexes = [x["refNumber"] for x in flight_indexes if x["refQualifier"] == 'S']
                for idx, val in enumerate(flight_indexes):
                    segments = []
                    flight_details = flights[idx]["groupOfFlights"][int(val) - 1]["flightDetails"]
                    flight_details = ensure_list(flight_details)
                    for leg, flight in enumerate(flight_details):
                        flight_info = from_json(flight, "flightInformation")
                        flight_number = from_json(flight_info, "flightOrtrainNumber")
                        locations = from_json(flight_info, "location")
                        locations = ensure_list(locations)
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
                        fare_details = ensure_list(rec["paxFareProduct"])[0]["fareDetails"]
                        fare_details = ensure_list(fare_details)
                        product_detail = ensure_list(fare_details[idx]["groupOfFares"])[leg]["productInformation"]
                        book_class = product_detail["cabinProduct"]["rbd"]
                        fare_basis = product_detail["fareProductDetail"]["fareBasis"]
                        segment = {"fare_basis": fare_basis, "board_airport": board_airport, "off_airport": off_airport,
                                   "flight_number": flight_number, "departure_date": departure_date,
                                   "departure_time": departure_time, "arrival_date": arrival_date,
                                   "arrival_time": arrival_time, "marketing_company": market_company,
                                   "operator_company": oper_company, "book_class": book_class
                                   }
                        segments.append(segment)
                    itineraries.append(segments)
                reco["itineraries"] = itineraries
                recs.append(reco)
        return recs


class AddMultiElementExtractor(BaseResponseExtractor):
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="PNR_Reply")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")
        pnr = from_json(payload, "pnrHeader", "reservationInfo", "reservation")
        pnr_data = {"pnr_number": pnr}
        travellers_info = from_json(payload, "travellerInfo")
        passengers = []
        travellers_info = ensure_list(travellers_info)
        for idx, pax in enumerate(travellers_info):
            info = from_json(pax, "passengerData", "travellerInformation")
            surname = from_json(info, "traveller", "surname")
            name = from_json(info, "passenger", "firstName")
            passenge_type = from_json(info, "passenger", "type")
            date_of_birth = ""
            passengers.append({"surname": surname, "name": name, "type": passenge_type, "date_of_birth": date_of_birth})
        pnr_data["passengers"] = passengers

        itineraries_info = from_json(payload, "originDestinationDetails", "itineraryInfo")
        itineraries_info = ensure_list(itineraries_info)
        segments = []
        for idx, seg in enumerate(itineraries_info):
            travel_details = from_json(seg, "travelProduct")
            from_city = from_json(travel_details, "boardpointDetail", "cityCode")
            to_city = from_json(travel_details, "offpointDetail", "cityCode")
            company = from_json(travel_details, "companyDetail", "identification")
            product = from_json(travel_details, "product")
            dep_date = from_json(product, "depDate")
            dep_time = from_json(product, "depTime")
            arr_date = from_json(product, "arrDate")
            arr_time = from_json(product, "arrTime")

            fligth_number = from_json(travel_details, "productDetails", "identification")
            segments.append({"from_city": from_city, "to_city": to_city, "company": company, "dep_date": dep_date,
                             "dep_time": dep_time, "arr_date": arr_date, "arr_time": arr_time,
                             "fligth_number": fligth_number})
        pnr_data["segments"] = segments
        return pnr_data


class PricePNRExtractor(BaseResponseExtractor):
    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="Fare_PricePNRWithBookingClassReply")
        self.parsed = True

    def default_value(self):
        return []

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Fare_PricePNRWithBookingClassReply")
        fare_list = from_json(payload, "fareList")
        fare_list = ensure_list(fare_list)
        fares = []
        for idx, fare in enumerate(fare_list):
            _fare = Fare()
            ref = fare["fareReference"]
            ref_type = ref["referenceType"]
            if ref_type.upper() == "TST":
                _fare.fare_reference = ref["uniqueReference"]
            places = from_json(fare, "originDestination", "cityCode")
            places = ensure_list(places)
            if len(places) != 2:
                self.log.error("The Origin destination must contain 2 elements")
            _fare.origin = places[0]
            _fare.destination = places[1]
            _fare.validating_carrier = from_json_safe(fare, "validatingCarrier", "carrierInformation", "carrierCode")
            _fare.banker_rate = from_json_safe(fare, "bankerRates", "firstRateDetail", "amount")
            _fare.pax_references = self._pax_refs(fare)
            _fare.fare_amounts = self._amounts(fare)
            _fare.tax_infos = self._taxes(fare)
            _fare.warning_infos = self._warnings(fare)
            _fare.fare_components = self._components(fare)
            _fare.segment_infos = self._segments(fare)
            fares.append(_fare)
        return fares

    def _pax_refs(self, fare):
        """
        look for passenger references
        :param fare: a dictionary containing fare info
        :return: List[str]
        """
        refs = []
        for pax_ref in ensure_list(from_json(fare, "paxSegReference", "refDetails")):
            if pax_ref["refQualifier"] == 'PA':
                refs.append(pax_ref["refNumber"])
        return refs

    def _amounts(self, fare):
        """
        look for amounts
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        amounts = []
        fare_amounts = from_json(fare, "fareDataInformation")
        fare_main = from_json(fare_amounts, "fareDataMainInformation")
        fare_amounts = ensure_list(from_json(fare_amounts, "fareDataSupInformation"))
        fare_amounts.append(fare_main)
        for am in fare_amounts:
            amounts.append(extract_amount(am))
        return amounts

    def _taxes(self, fare):
        """
        look for taxes
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        taxes = []
        for tax_info in ensure_list(from_json(fare, "taxInformation")):
            tax: TaxInformation = TaxInformation()
            tax_details = from_json(tax_info, "taxDetails")
            tax.tax_qualifier = from_json_safe(tax_details, "taxQualifier")
            tax.tax_identifier = from_json_safe(tax_details, "taxIdentification", "taxIdentifier")
            tax.tax_type = from_json_safe(tax_details, "taxType", "isoCountry")
            tax.tax_nature = from_json_safe(tax_details, "taxNature")
            tax.tax_amount = extract_amount(from_json(tax_info, "amountDetails", "fareDataMainInformation"))
            taxes.append(tax)
        return taxes

    def _warnings(self, fare):
        """
        look for warnings
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        warnings = []
        for warning_info in ensure_list(from_json(fare, "warningInformation")):
            warning: WarningInformation = WarningInformation()
            details = from_json_safe(warning_info, "warningCode", "applicationErrorDetail")
            warning.error_code = from_json_safe(details, "applicationErrorCode")
            warning.qualifier = from_json_safe(details, "codeListQualifier")
            warning.responsible_agency = from_json_safe(details, "codeListResponsibleAgency")
            warning.warning = from_json_safe(warning_info, "warningText", "errorFreeText")
            warnings.append(warning)
        return warnings

    def _components(self, fare):
        """
        look for components
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        components = []
        for comp in ensure_list(from_json(fare, "fareComponentDetailsGroup")):
            fare_component: FareComponent = FareComponent()
            item_details = from_json_safe(comp, "fareComponentID", "itemNumberDetails")
            fare_component.item_number = from_json_safe(item_details, "number")
            fare_component.item_type = from_json_safe(item_details, "type")

            places = from_json(comp, "marketFareComponent")
            fare_component.departure = from_json(places, "boardPointDetails", "trueLocationId")
            fare_component.arrival = from_json(places, "offpointDetails", "trueLocationId")
            fare_component.monetary_info = extract_amount(
                from_json_safe(comp, "monetaryInformation", "monetaryDetails"),
                "typeQualifier", "amount", "currency")
            fare_component.rate_tariff_class = from_json_safe(comp, "componentClassInfo", "fareBasisDetails",
                                                              "rateTariffClass")
            fare_component.fare_qualifier = from_json_safe(comp, "fareQualifiersDetail", "discountDetails",
                                                           "fareQualifier")
            f_details = from_json_safe(comp, "fareFamilyDetails")
            fare_component.fare_family_name = from_json_safe(f_details, "fareFamilyname")
            fare_component.fare_family_hierarchy = from_json_safe(f_details, "hierarchy")
            fare_component.fare_family_owner = from_json_safe(comp, "fareFamilyOwner", "companyIdentification",
                                                              "otherCompany")
            # let's get coupons
            for coupon_info in ensure_list(from_json_safe(comp, "couponDetailsGroup")):
                coupon: CouponDetails = CouponDetails()
                info = from_json_safe(coupon_info, "productId", "referenceDetails")
                coupon.coupon_product_type = from_json_safe(info, "type")
                coupon.coupon_product_id = from_json_safe(info, "value")
                fare_component.coupons.append(coupon)
            components.append(fare_component)
        return components

    def _segments(self, fare):
        """
        look for segments
        :param fare: a dictionary containing fare info
        :return: List[Amount]
        """
        segments = []
        for sg in ensure_list(from_json(fare, "segmentInformation")):
            segment: SegmentInformation = SegmentInformation()
            s_ref = from_json(sg, "segmentReference", "refDetails")
            if s_ref and s_ref["refQualifier"] == "S":
                segment.segment_reference = s_ref["refNumber"]
            segment.segment_sequence_number = from_json_safe(sg, "sequenceInformation", "sequenceSection",
                                                             "sequenceNumber")
            segment.connection_type = from_json(sg, "connexInformation", "connecDetails", "connexType")
            segment.class_of_service = from_json(sg, "segDetails", "segmentDetail", "classOfService")

            fare_basis = from_json(sg, "fareQualifier", "fareBasisDetails")
            segment.fare_basis_primary_code = from_json(fare_basis, "primaryCode")
            segment.fare_basis_code = from_json(fare_basis, "fareBasisCode")
            segment.fare_basis_ticket_designator = from_json(fare_basis, "discTktDesignator")

            baggage_allowance = from_json(sg, "bagAllowanceInformation", "bagAllowanceDetails")
            segment.baggage_allowance_quantity = from_json(baggage_allowance, "baggageQuantity")
            segment.baggage_allowance_type = from_json(baggage_allowance, "baggageType")

            for validity in ensure_list(from_json_safe(sg, "validityInformation")):
                validity_info: ValidityInformation = ValidityInformation()
                validity_info.business_semantic = from_json_safe(validity, "businessSemantic")
                dt = from_json_safe(validity, "dateTime")
                if dt:
                    validity_info.date = f"{dt['year']}-{dt['month']}-{dt['day']}"
                segment.validity_infos.append(validity_info)
            segments.append(segment)
        return segments


class CommandReplyExtractor(BaseResponseExtractor):
    """
        Class command reply from XML Response
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, main_tag="Command_CrypticReply")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Command_CrypticReply")
        return from_json(payload, "longTextString", "textStringDetails")


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
        super().__init__(xml_content, True, True, "PNR_Reply")
        self.parsed = True

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")
        self.payload = payload
        # print(payload)
        return {
            'pnr_info': self._pnr_info()
            # 'passengers': self._passengers()
            # 'itineraries': self._segments(),
            # 'form_of_payments': self._form_of_payments(),
            # 'price_quotes': self._price_quotes(),
            # 'ticketing_info': self._ticketing_info(),
            # 'remarks': self._remark()
        }

    def _segments(self):
        segments_list = []
        index = 1
        for data in ensure_list(from_json_safe(self.payload, "originDestinationDetails", "itineraryInfo")):
            dep_date = from_json_safe(data, "travelProduct", "product", "depDate")
            dep_time = from_json_safe(data, "travelProduct", "product", "depTime")
            arr_date = from_json_safe(data, "travelProduct", "product", "arrDate")
            arr_time = from_json_safe(data, "travelProduct", "product", "arrTime")
            departure_airport = from_json_safe(data, "travelProduct", "boardpointDetail", "cityCode")
            airline_code_marketing = from_json_safe(data, "itineraryReservationInfo", "reservation", "companyId")
            airline_code_operat = from_json_safe(data, "itineraryReservationInfo", "reservation", "companyId")
            flight_number_airline_mark = from_json_safe(data, "travelProduct", "productDetails", "identification")
            control_number = from_json_safe(data, "itineraryReservationInfo", "reservation", "controlNumber")
            flight_number_airline_operat = from_json_safe(data, "travelProduct", "productDetails", "identification")
            arrival_airport = from_json_safe(data, "travelProduct", "offpointDetail", "cityCode")
            company_id = from_json_safe(data, "itineraryReservationInfo", "reservation", "companyId")
            quantity = from_json_safe(data, "relatedProduct", "quantity")
            status = from_json_safe(data, "relatedProduct", "status")
            segment_reference = from_json_safe(data, "elementManagementItinerary", "reference", "number")
            departure_date_time = reformat_date(dep_date + dep_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            arrival_date_time = reformat_date(arr_date + arr_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            equipment_type = data["flightDetail"]["productDetails"]["equipment"]
            resbook_designator = data["travelProduct"]["productDetails"]["classOfService"]
            departure_terminal = None  # from_json_safe("flightDetail", "departureInformation", "departTerminal")
            arrival_terminal = None  # from_json_safe("flightDetail", "arrivalStationInfo", "terminal")
            departure = FlightPointDetails("", departure_airport, departure_terminal)
            arrival = FlightPointDetails("", arrival_airport, arrival_terminal)
            marketing_airline = FlightAirlineDetails(airline_code_marketing, flight_number_airline_mark, "", control_number)
            operating_airline = FlightAirlineDetails(airline_code_operat, flight_number_airline_operat, "", control_number)
            segment_data = FlightSegment(index, resbook_designator, departure_date_time, departure, arrival_date_time, arrival, status, company_id, quantity, marketing_airline, operating_airline, "", "", "", "", "", "", "", "", "", "", "", equipment_type, "", "")
            segment_data.segment_reference = segment_reference
            index += 1
            segments_list.append(segment_data)
        return segments_list

    def _date_of_birth(self):
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            ssr = from_json_safe(data, "serviceRequest", "ssr")
            if ssr and from_json_safe(ssr, "type") == "DOCS":
                free_text = from_json_safe(ssr, "freeText")
                if free_text:
                    check_date_of_birth = re.split("[, /,////?//:; ]+", free_text)  # to transform the caracter chaine in liste_object
                    print(check_date_of_birth)
                    if len(check_date_of_birth) >= 2:
                        check_date_of_birth = check_date_of_birth[1]
                        return check_date_of_birth
        return None

    def _gender(self):
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            ssr = from_json_safe(data, "serviceRequest", "ssr")
            if ssr and from_json_safe(ssr, "type") == "DOCS":
                free_text = from_json_safe(ssr, "freeText")
                if free_text:
                    check_gender = re.split("[, /,////?//:; ]+", free_text)  # to transform the caracter chaine in liste_object
                    if len(check_gender) >= 3:
                        check_gender = check_gender[2]
                        if check_gender == "M" or check_gender == "F":
                            return check_gender
        return None

    def _passengers(self):
        passengers_list = []
        date_of_bt = self._date_of_birth()
        gender = self._gender()
        for traveller in ensure_list(from_json(self.payload, "travellerInfo")):
            ref = from_json_safe(traveller, "elementManagementPassenger", "reference", "number")
            data = from_json_safe(traveller, "passengerData")
            traveller_info = from_json_safe(data, "travellerInformation")
            psngr = from_json_safe(traveller_info, "passenger")
            travel = from_json_safe(traveller_info, "traveller")
            # date_of_birth_tag = from_json_safe(data, "dateOfBirth", "dateAndTimeDetails", "date")
            # date_of_birth = reformat_date(date_of_birth_tag, "%d%m%Y", "%Y-%m-%d") if date_of_birth_tag else None
            firstname = from_json_safe(psngr, "firstName")
            lastname = from_json_safe(travel, "surname")
            surname = from_json_safe(travel, "surname")
            forename = from_json_safe(psngr, "firstName")
            number_in_party = from_json_safe(travel, "quantity")
            if psngr and from_json_safe(psngr, "type"):
                type_passenger = from_json_safe(psngr, "type")
            else:
                type_passenger = "ADT"
            passsenger = Passenger(ref, firstname, lastname, date_of_bt, gender, surname, forename, "", "", number_in_party, "", type_passenger, "")
            passengers_list.append(passsenger)
        return passengers_list

    def _dk_number(self):
        dk = ""
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            if "accounting" in data:
                data_account = from_json(data, "accounting")
                dk = from_json_safe(data_account, "account", "number")
        return dk

    def _pnr_info(self):
        dk = self._dk_number()
        dk_list = []
        for data in ensure_list(from_json_safe(self.payload, "securityInformation", "secondRpInformation")):
            agent_signature = from_json_safe(data, "agentSignature")
            creation_office_id = from_json_safe(data, "creationOfficeId")
            creation_date = from_json_safe(data, "creationDate")
            creation_time = from_json_safe(data, "creationTime")
            creation_date_time = reformat_date(creation_date + creation_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            pnr = PnrInfo(dk, agent_signature, creation_office_id, creation_date_time)
            dk_list.append(pnr)
        return dk_list

    def _price_quotes(self):
        price_quotes = []
        pqs = from_json_safe(self.payload, "pricingRecordGroup", "productPricingQuotationRecord")
        pqs = ensure_list(pqs)
        for data in pqs:
            price_quotes_details = {
                'pricing_record_id': data['pricingRecordId'],
                'passenger_tattoos': data['passengerTattoos'],
                'total_fare': data['documentDetailsGroup']['totalFare']
            }
            price_quotes.append(price_quotes_details)
        return price_quotes

    def _form_of_payments(self):
        list_form_payment = []
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            element_management_data = from_json_safe(data, "elementManagementData")
            if element_management_data["segmentName"] == "FP":
                other_details = from_json_safe(data, "otherDataFreetext")
                text = from_json_safe(other_details, "longFreetext")
                form_payment = FormOfPayment("", text, "", "")
                list_form_payment.append(form_payment)
        return list_form_payment

    def _ticketing_info(self):
        list_ticket = []
        for ticket in ensure_list(from_json_safe(self.payload["dataElementsMaster"], "dataElementsIndiv")):
            for elem_tick in ticket:
                if "ticketElement" in elem_tick:
                    data_element = from_json_safe(ticket, "ticketElement")
                    ticket_element = from_json_safe(data_element, "ticket")
                    element_id = from_json_safe(ticket_element, "officeId")
                    date = from_json_safe(ticket_element, "date")
                    comment = from_json_safe(ticket_element, "indicator")
                    code = from_json_safe(ticket_element, "airlineCode")
                    ticketing = TicketingInfo(element_id, "", "", code, "", date, "", "", comment)
                    list_ticket.append(ticketing)
        return list_ticket

    def _remark(self):
        list_remark = []
        sequence = 1
        for data_element in ensure_list(from_json_safe(self.payload["dataElementsMaster"], "dataElementsIndiv")):
            data_remarks = from_json_safe(data_element, "miscellaneousRemarks")
            if data_remarks and from_json_safe(data_remarks, "remarks", "type") == "RM":
                rems = from_json_safe(data_remarks, "remarks")
                remark_type = from_json_safe(rems, "type")
                categorie = from_json_safe(rems, "category")
                text = from_json_safe(rems, "freetext")
                remarks_object = Remarks(sequence, remark_type, categorie, text)
                sequence += 1
                list_remark.append(remarks_object)
        return list_remark


class CreateTstResponseExtractor(BaseResponseExtractor):
    """
    Wil extract response of create TST from price
    """

    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "Ticket_CreateTSTFromPricingReply")

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Ticket_CreateTSTFromPricingReply")
        pnr = from_json_safe(payload, "pnrLocatorData", "reservationInformation", "controlNumber")
        tst_data = from_json(payload, "tstList")
        tst_ref_data = from_json(tst_data, "tstReference")
        tst_ref = None
        if from_json_safe(tst_ref_data, "referenceType") == "TST":
            tst_ref = from_json_safe(tst_ref_data, "uniqueReference")
        passengers_data = ensure_list(from_json(tst_data, "paxInformation", "refDetails"))
        pax_refs = []
        for p in passengers_data:
            pax_refs.append(from_json(p, "refNumber"))
        return TstInformation(pnr, tst_ref, pax_refs)


class IssueTicketResponseExtractor(BaseResponseExtractor):
    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "DocIssuance_IssueTicketReply")

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "DocIssuance_IssueTicketReply")
        status = from_json_safe(payload, "processingStatus", "statusCode")
        error_data = from_json_safe(payload, "errorGroup")
        if error_data:
            error_code = from_json_safe(error_data, "errorOrWarningCodeDetails", "errorDetails", "errorCode")
            details = from_json_safe(error_data, "errorWarningDescription")
            description = from_json_safe(details, "freeText")
            details = from_json_safe(details, "freeTextDetails")
            qualifier = from_json_safe(details, "textSubjectQualifier")
            source = from_json_safe(details, "source")
            encoding = from_json_safe(details, "encoding")
        else:
            error_code, qualifier, source, encoding, description = (None, None, None, None, None)
        return TicketReply(status, error_code, qualifier, source, encoding, description)


def extract_amount(amount_info, type_key="fareDataQualifier", amount_key="fareAmount",
                   currency_key="fareCurrency") -> FareAmount:
    fare_amount = FareAmount()
    fare_amount.qualifier = from_json_safe(amount_info, type_key)
    fare_amount.amount = from_json_safe(amount_info, amount_key)
    fare_amount.currency = from_json_safe(amount_info, currency_key)
    return fare_amount
