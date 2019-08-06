import re
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor, extract_amount
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe, ensure_list, \
    get_data_from_xml as from_xml, reformat_date
from pygds.core.price import FareElement, TaxInformation, FareAmount
from pygds.core.types import FlightPointDetails, FlightAirlineDetails, FlightSegment, Passenger, PnrInfo, Remarks, \
    TicketingInfo, FormOfPayment


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
        return {
            'passengers': self._passengers(),
            'itineraries': self._segments(),
            'form_of_payments': self._form_of_payments(),
            'price_quotes': self._price_quotes(),
            'tst_data': self._tst_data(),
            'ticketing_info': self._ticketing_info(),
            'remarks': self._remark(),
            'pnr_info': self._pnr_info()
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
            flight_number_airline_operat = from_json_safe(data, "travelProduct", "productDetails", "identification")
            arrival_airport = from_json_safe(data, "travelProduct", "offpointDetail", "cityCode")
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
            marketing_airline = FlightAirlineDetails(airline_code_marketing, flight_number_airline_mark, "")
            operating_airline = FlightAirlineDetails(airline_code_operat, flight_number_airline_operat, "")
            segment_data = FlightSegment(index, resbook_designator, departure_date_time, departure, arrival_date_time, arrival, status, quantity, marketing_airline, operating_airline, "", "", "", "", "", "", "", "", "", "", "", equipment_type, "", "")
            segment_data.segment_reference = segment_reference
            index += 1
            segments_list.append(segment_data)
        return segments_list

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
        gender = self._gender()
        for traveller in ensure_list(from_json(self.payload, "travellerInfo")):
            ref = from_json_safe(traveller, "elementManagementPassenger", "reference", "number")
            data = from_json_safe(traveller, "passengerData")
            traveller_info = from_json_safe(data, "travellerInformation")
            psngr = from_json_safe(traveller_info, "passenger")
            travel = from_json_safe(traveller_info, "traveller")
            date_of_birth_tag = from_json_safe(data, "dateOfBirth", "dateAndTimeDetails", "date")
            date_of_birth = reformat_date(date_of_birth_tag, "%d%m%Y", "%Y-%m-%d") if date_of_birth_tag else None
            firstname = from_json_safe(psngr, "firstName")
            lastname = from_json_safe(travel, "surname")
            surname = from_json_safe(travel, "surname")
            forename = from_json_safe(psngr, "firstName")
            number_in_party = from_json_safe(travel, "quantity")
            type_passenger = from_json_safe(psngr, "type")
            passsenger = Passenger(ref, firstname, lastname, date_of_birth, gender, surname, forename, "", "", number_in_party, "", type_passenger, "")
            passengers_list.append(passsenger)
        return passengers_list

    def _dk_number(self):
        dk = ""
        for data in ensure_list(from_json(self.payload, "dataElementsMaster", "dataElementsIndiv")):
            if "accounting" in data:
                data_account = from_json(data, "accounting")
                dk = from_json_safe(data_account, "account", "number")
        return dk

    def _pnr_info(self):
        dk_number = self._dk_number()
        pnr_infos = []
        for data in ensure_list(from_json_safe(self.payload, "originDestinationDetails", "itineraryInfo")):
            dep_date = from_json_safe(data, "travelProduct", "product", "depDate")
            dep_time = from_json_safe(data, "travelProduct", "product", "depTime")
            arr_date = from_json_safe(data, "travelProduct", "product", "arrDate")
            arr_time = from_json_safe(data, "travelProduct", "product", "arrTime")
            departure_airport = from_json_safe(data, "travelProduct", "boardpointDetail", "cityCode")
            company_id = from_json_safe(data, "itineraryReservationInfo", "reservation", "companyId")
            control_number = from_json_safe(data, "itineraryReservationInfo", "reservation", "controlNumber")
            departure_date_time = reformat_date(dep_date + dep_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            arrival_date_time = reformat_date(arr_date + arr_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            arrival_airport = from_json_safe(data, "travelProduct", "offpointDetail", "cityCode")
            info_pnr = PnrInfo(company_id, control_number, dk_number, departure_date_time, arrival_date_time, departure_airport, arrival_airport)
            pnr_infos.append(info_pnr)
        return pnr_infos

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

    def _tst_data(self):
        tst_data = from_json_safe(self.payload, "tstData")
        if tst_data:
            fare_elements = []
            taxes = []
            total_taxes = 0.0
            total_taxes_currency = None
            amounts = []
            pax_refs = []
            segment_refs = []
            base_fare = None
            total_fare = None
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

            for am in ensure_list(from_json_safe(tst_data, "fareData", "monetaryInfo")):
                am = extract_amount(am, "qualifier", "amount", "currencyCode")
                if am.qualifier == "F" and not base_fare:
                    base_fare = am
                if am.qualifier == "E":
                    base_fare = am
                elif am.qualifier == "T":
                    total_fare = am
                amounts.append(am)

            for tax_info in ensure_list(from_json(tst_data, "fareData", "taxFields")):
                tax: TaxInformation = TaxInformation()
                # tax.tax_qualifier = from_json_safe(tax_info, "taxIndicator")
                # tax.tax_identifier = from_json_safe(tax_info, "taxIndicator")
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

            for ref in ensure_list(from_json_safe(tst_data, "referenceForTstData", "reference")):
                qualifier, reference = (from_json_safe(ref, "qualifier"), from_json_safe(ref, "number"))
                if qualifier == "PT":
                    pax_refs.append(reference)
                elif qualifier == "ST":
                    segment_refs.append(reference)
            return {
                "passenger_references": pax_refs,
                "base_fare": base_fare.to_dict() if base_fare else None,
                "total_fare": total_fare.to_dict() if total_fare else None,
                "total_taxes": total_taxes.to_dict(),
                "segment_references": segment_refs,
                "amounts": [am.to_dict() for am in amounts],
                "taxes": [ta.to_dict() for ta in taxes],
                "fare_elements": [fe.to_dict() for fe in fare_elements]
            }

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
        for ticket in ensure_list(from_json(self.payload["dataElementsMaster"], "dataElementsIndiv")):
            for elem_tick in ticket:
                if "ticketElement" in elem_tick:
                    data_element = from_json(ticket, "ticketElement")
                    ticket_element = from_json(data_element, "ticket")
                    element_id = from_json(ticket_element, "officeId")
                    date = from_json(ticket_element, "date")
                    comment = from_json(ticket_element, "indicator")
                    code = from_json_safe(ticket_element, "airlineCode")
                    ticketing = TicketingInfo(element_id, "", "", code, "", date, "", "", comment)
                    list_ticket.append(ticketing)
        return list_ticket

    def _remark(self):
        list_remark = []
        sequence = 1
        for data_element in ensure_list(from_json(self.payload["dataElementsMaster"], "dataElementsIndiv")):
            for remarks in data_element:
                if "miscellaneousRemarks" in remarks:
                    data_remarks = from_json(remarks, "miscellaneousRemarks")
                    print(data_remarks)
                    rems = from_json(data_remarks, "remarks")
                    remark_type = from_json(rems, "type")
                    category = from_json(rems, "category")
                    text = from_json(rems, "freetext")
                    remarks_object = Remarks(sequence, remark_type, category, text)
                    sequence += 1
                    list_remark.append(remarks_object)
                else:
                    return None
        return list_remark
