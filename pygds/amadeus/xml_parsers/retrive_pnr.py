import re
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor, extract_amount
from pygds.core.helpers import get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml, reformat_date
from pygds.core.price import FareElement, TaxInformation, FareAmount
from pygds.core.types import FlightPointDetails, FlightAirlineDetails, FlightSegment, Passenger, Remarks, \
    FormOfPayment, PnrInfo, PnrHeader, FormatAmount, FormatPassengersInPQ, PriceQuote_, TicketingInfo_
import fnc


class GetPnrResponseExtractor(BaseResponseExtractor):
    """
        A class to extract Reservation from response of retrieve PNR.
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, True, True, "PNR_Reply")
        self.parsed = True
        self.payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")

    def _extract(self):
        return {
            'passengers': self.get_all_passengers,
            'itineraries': self._segments(),
            'form_of_payments': self._form_of_payments(),
            'price_quotes': self.price_quotes,
            'ticketing_info': self.get_ticketing_info,
            'remarks': self._remark(),
            'pnr_info': self._pnr_info(),
            'dk_number': self._dk_number(),
        }

    def _ot_info(self):
        ot_informations = from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")
        return ot_informations

    def _pnr_header(self):
        pnr_header = from_json_safe(self.payload, "pnrHeader", "reservationInfo", "reservation")
        if isinstance(pnr_header, dict):
            controle_number = from_json_safe(pnr_header, "controlNumber")
            company_id = from_json_safe(pnr_header, "companyId")
            creation_date = from_json_safe(pnr_header, "date")
            creation_time = from_json_safe(pnr_header, "time")
            return PnrHeader(controle_number, company_id, creation_date, creation_time)
        return None

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
            # company_id = from_json_safe(data, "itineraryReservationInfo", "reservation", "companyId")
            # quantity = from_json_safe(data, "relatedProduct", "quantity")
            status = from_json_safe(data, "relatedProduct", "status")
            if isinstance(status, list):
                status = status[0]  # we need to recover the first item if status is a list
            else:
                status = status
            segment_reference = from_json_safe(data, "elementManagementItinerary", "reference", "number")
            departure_date_time = reformat_date(dep_date + dep_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            arrival_date_time = reformat_date(arr_date + arr_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            equipment_type = data["flightDetail"]["productDetails"]["equipment"]
            resbook_designator = data["travelProduct"]["productDetails"]["classOfService"]
            departure_terminal = None  # from_json_safe("flightDetail", "departureInformation", "departTerminal")
            arrival_terminal = None  # from_json_safe("flightDetail", "arrivalStationInfo", "terminal")
            departure = FlightPointDetails(departure_date_time, departure_airport, departure_terminal)
            arrival = FlightPointDetails(arrival_date_time, arrival_airport, arrival_terminal)
            marketing_airline = FlightAirlineDetails(airline_code_marketing, flight_number_airline_mark, "", control_number)
            operating_airline = FlightAirlineDetails(airline_code_operat, flight_number_airline_operat, "", control_number)
            segment_data = FlightSegment(index, resbook_designator, departure_date_time, departure, arrival_date_time, arrival, status, marketing_airline, operating_airline, "", "", "", "", "", "", "", "", "", "", "", "", "", equipment_type, "", "")
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
                    if len(check_date_of_birth) >= 2:
                        check_date_of_birth = check_date_of_birth[1]
                        data_date_of_birth = reformat_date(check_date_of_birth, "%d%b%y", "%Y-%m-%d")
                        return data_date_of_birth
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

    @property
    def get_all_passengers(self):
        all_passengers = []

        for traveller in ensure_list(
            fnc.get("travellerInfo", self.payload, default=[])
        ):
            reference = fnc.get("elementManagementPassenger.reference.number", traveller)
            all_passenger_data = ensure_list(fnc.get("passengerData", traveller, default=[]))

            for index, passenger in enumerate(fnc.get(
                "enhancedPassengerData", traveller, default=[]
            )):
                date_of_birth = fnc.get(
                    "dateOfBirthInEnhancedPaxData.dateAndTimeDetails.date", passenger
                )
                surname = fnc.get(
                    "enhancedTravellerInformation.otherPaxNamesDetails.surname", passenger)
                given_name = fnc.get(
                    "enhancedTravellerInformation.otherPaxNamesDetails.givenName", passenger)
                passenger_type = fnc.get(
                    "enhancedTravellerInformation.travellerNameInfo.type", passenger
                )
                firstname = fnc.get(
                    "travellerInformation.passenger.firstName", all_passenger_data[index] if len(all_passenger_data) > index else {}
                )
                number_in_party = fnc.get(
                    "travellerInformation.traveller.quantity", all_passenger_data[index] if len(all_passenger_data) > index else {}
                )

                passsenger = Passenger(reference, "", firstname, None, date_of_birth, None, surname, given_name, "", "",
                                       number_in_party, "", passenger_type, "", {})
                all_passengers.append(passsenger)
        return all_passengers

    def _dk_number(self):
        dk = ""
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            if "accounting" in data:
                data_account = from_json_safe(data, "accounting")
                dk = from_json_safe(data_account, "account", "number")
        return dk

    def pnr_info(self):
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

    @property
    def get_price_quotes(self):
        all_price_quote = []

        for tst in self._tst_data():
            all_passengers = []
            pq_number = 0
            status = None
            fare_type = None
            base_fare = tst["base_fare"] if "base_fare" in tst else None
            if base_fare:
                base_fare_value = float(base_fare["amount"])
                base_fare_cc = base_fare["currency"]
            else:
                base_fare_value = None
                base_fare_cc = None

            base_fare = FormatAmount(base_fare_value, base_fare_cc).to_data()

            total_fare = tst["total_fare"] if "total_fare" in tst else None
            if total_fare:
                total_fare_value = float(total_fare["amount"])
                total_fare_cc = total_fare["currency"]
            else:
                total_fare_value = None
                total_fare_cc = None

            total_fare = FormatAmount(total_fare_value, total_fare_cc).to_data()

            total_taxes = tst["total_taxes"] if "total_taxes" in tst else None
            if total_taxes:
                tax_fare_value = float(total_taxes["amount"])
                tax_fare_cc = total_taxes["currency"]
            else:
                tax_fare_value = None
                tax_fare_cc = None

            tax_fare = FormatAmount(tax_fare_value, tax_fare_cc).to_data()
            validating_carrier = None
            commission_percentage = None

            for passenger in tst["passenger_references"] if "passenger_references" in tst else []:
                passenger = FormatPassengersInPQ(
                    passenger["name_id"] if "name_id" in passenger else None, passenger["type"] if "type" in passenger else None
                ).to_data()
                all_passengers.append(passenger)

            price_quote_data = PriceQuote_(int(pq_number), status, fare_type, base_fare, total_fare, tax_fare, validating_carrier, all_passengers, commission_percentage)
            all_price_quote.append(price_quote_data)

        return all_price_quote

    def _form_of_payments(self):
        list_form_payment = []
        for data in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            element_management_data = from_json_safe(data, "elementManagementData")
            if element_management_data["segmentName"] == "FP":
                other_details = from_json_safe(data, "otherDataFreetext")
                text = from_json_safe(other_details, "longFreetext")
                form_payment = FormOfPayment(text)
                list_form_payment.append(form_payment)
        return list_form_payment

    def _extract_qualifier_number(self, list_reference):
        qualifier, number = "", ""
        list_reference = ensure_list(list_reference)
        for reference in list_reference:
            if reference["qualifier"] == "PT":
                qualifier = reference["qualifier"]
                number = reference["number"]
        return qualifier, number

    @property
    def get_ticketing_info(self):
        """
        This method is to return a list of ticket
        return list_ticket
        """
        all_ticket = []
        agency_location = None
        time_stamp = None
        transaction_indicator = None
        for ticket in ensure_list(
            fnc.get(
                "dataElementsIndiv", fnc.get("dataElementsMaster", self.payload, default={}), default=[]
            )
        ):
            if "ticketElement" in ticket:
                agency_location = fnc.get("ticketElement.ticket.officeId", ticket)
                time_stamp = fnc.get("ticketElement.ticket.date", ticket)
                transaction_indicator = fnc.get("ticketElement.ticket.indicator", ticket)

            if fnc.get("elementManagementData.segmentName", ticket) in ["FA"]:
                list_reference = fnc.get(
                    "reference", ticket["referenceForDataElement"] if "referenceForDataElement" in ticket else {}
                )
                qualifier, name_id = self._extract_qualifier_number(list_reference)
                passenger = self.get_passenger(name_id)

                full_name = (passenger.first_name if passenger.first_name else "") + " " + (passenger.last_name if passenger.last_name else "") if passenger else None
                full_ticket_number = fnc.get(
                    "longFreetext", ticket["otherDataFreetext"] if "otherDataFreetext" in ticket else {}
                )
                index = fnc.get("elementManagementData.reference.number", ticket)

                ticket_number = self.get_ticket_number(full_ticket_number)

                ticketing = TicketingInfo_(
                    ticket_number, transaction_indicator, name_id, agency_location, time_stamp, index, full_ticket_number, "", full_name
                )

                all_ticket.append(ticketing)
        return all_ticket

    def get_passenger(self, name_id):
        for passenger in self.get_all_passengers:
            if passenger.name_id == name_id:
                return passenger

        return None

    def get_ticket_number(self, ticket_number: str):
        if not ticket_number:
            return ""
        # PAX 080-7421982399/ETLO/USD126.39/29NOV19/DTW1S210B/23612444
        split_value = ticket_number.split(" ")
        value = split_value[len(split_value) - 1]
        return value.split("/")[0]

    def _remark(self):
        list_remark = []
        sequence = 1
        for data_element in ensure_list(from_json_safe(self.payload, "dataElementsMaster", "dataElementsIndiv")):
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

    def _tst_data(self):
        all_tst = []
        for tst_data in ensure_list(
            fnc.get("tstData", self.payload, default=[])
        ):
            fare_elements = self._tst_fare_elements(tst_data)
            total_taxes, taxes = self._tst_taxes(tst_data)
            pax_refs, segment_refs = self._tst_pax_segs_refs(tst_data)
            base_fare, total_fare, amounts = self._tst_amounts(tst_data)

            tst = {
                "passenger_references": pax_refs,
                "base_fare": base_fare.to_dict() if base_fare else None,
                "total_fare": total_fare.to_dict() if total_fare else None,
                "total_taxes": total_taxes.to_dict(),
                "segment_references": segment_refs,
                "amounts": [am.to_dict() for am in amounts],
                "taxes": [ta.to_dict() for ta in taxes],
                "fare_elements": [fe.to_dict() for fe in fare_elements]
            }
            all_tst.append(tst)
        return all_tst

    def _tst_pax_segs_refs(self, tst_data):
        pax_refs = []
        segment_refs = []
        passengers = self.get_all_passengers

        for ref in ensure_list(from_json_safe(tst_data, "referenceForTstData", "reference")):
            qualifier, reference = (from_json_safe(ref, "qualifier"), from_json_safe(ref, "number"))
            if qualifier == "PT":
                pax_refs.append(reference)
            elif qualifier == "ST":
                segment_refs.append(reference)

        return [
            {
                "name_id": passenger.name_id,
                "type": passenger.passenger_type
            } for passenger in passengers if passenger.name_id in pax_refs], segment_refs

    def _tst_fare_elements(self, tst_data):
        fare_elements = []
        for fe in ensure_list(from_json_safe(tst_data, "fareBasisInfo", "fareElement")):
            p_code = from_json_safe(fe, "primaryCode")
            connx = from_json_safe(fe, "connection")
            n_valid_b = from_json_safe(fe, "notValidBefore")
            n_valid_b = reformat_date(n_valid_b, "%d%m%y", "%Y-%m-%d") if n_valid_b else None
            n_valid_a = from_json_safe(fe, "notValidAfter")
            n_valid_a = reformat_date(n_valid_a, "%d%m%y", "%Y-%m-%d") if n_valid_a else None
            b_allow = from_json_safe(fe, "baggageAllowance")
            f_basis = from_json_safe(fe, "fareBasis")
            f_el = FareElement(p_code, connx, n_valid_b, n_valid_a, b_allow, f_basis)
            fare_elements.append(f_el)
        return fare_elements

    def _tst_amounts(self, tst_data):
        amounts = []
        base_fare = None
        total_fare = None
        for am in ensure_list(from_json_safe(tst_data, "fareData", "monetaryInfo")):
            am = extract_amount(am, "qualifier", "amount", "currencyCode")
            if am.qualifier == "F" and not base_fare:
                base_fare = am
            if am.qualifier == "E":
                base_fare = am
            elif am.qualifier == "T":
                total_fare = am
            amounts.append(am)
        return base_fare, total_fare, amounts

    def _tst_taxes(self, tst_data):
        total_taxes = 0.0
        total_taxes_currency = None
        taxes = []
        for tax_info in ensure_list(from_json_safe(tst_data, "fareData", "taxFields")):
            tax: TaxInformation = TaxInformation()
            tax.tax_type = from_json_safe(tax_info, "taxCountryCode")
            tax.tax_nature = from_json_safe(tax_info, "taxNatureCode")
            am = extract_amount(tax_info, "taxIndicator", "taxAmount", "taxCurrency")
            tax.tax_amount = am
            if not total_taxes_currency:
                total_taxes_currency = am.currency
            if am.currency == total_taxes_currency:  # avoid summing amounts on different currencies
                total_taxes += float(am.amount)
            taxes.append(tax)
        total_taxes = FareAmount(None, total_taxes, total_taxes_currency)
        return total_taxes, taxes
