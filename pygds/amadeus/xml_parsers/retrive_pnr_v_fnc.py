import re
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor, extract_amount
from pygds.core.helpers import ensure_list, get_data_from_xml as from_xml, reformat_date
from pygds.core.price import FareElement, TaxInformation, FareAmount
from pygds.core.types import FlightPointDetails, FlightAirlineDetails, FlightSegment, Passenger, Remarks, \
    InfoPaymentCreditCard, FormatAmount, FormatPassengersInPQ, PriceQuote_, TicketingInfo_, Itinerary, FlightDisclosureCarrier, FlightMarriageGrp
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
            'itineraries': self.get_segments,
            'form_of_payments': self.get_form_of_payments,
            'price_quotes': self.get_price_quotes,
            'ticketing_info': self.get_ticketing_info,
            'remarks': self.get_remarks,
            'dk_number': self.get_dk_number,
            "record_locator": fnc.get("pnrHeader.reservationInfo.reservation.controlNumber", self.payload),
            "booking_source": fnc.get("securityInformation.secondRpInformation.creationOfficeId", self.payload),
        }

    @property
    def get_segments(self):
        all_itineraries = []
        for itinerary in ensure_list(
            fnc.get("originDestinationDetails", self.payload, default=[])
        ):
            itinerary_object = Itinerary()
            for segment in ensure_list(
                fnc.get("itineraryInfo", itinerary, default=[])
            ):
                dep_date = fnc.get("travelProduct.product.depDate", segment)
                dep_time = fnc.get("travelProduct.product.depTime", segment)
                arr_date = fnc.get("travelProduct.product.arrDate", segment)
                arr_time = fnc.get("travelProduct.product.arrTime", segment)

                departure_date_time = reformat_date(
                    dep_date + dep_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S"
                ) if dep_date and dep_time else None
                arrival_date_time = reformat_date(
                    arr_date + arr_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S"
                ) if arr_date and arr_time else None

                departure_airport = fnc.get("travelProduct.boardpointDetail.cityCode", segment)
                arrival_airport = fnc.get("travelProduct.offpointDetail.cityCode", segment)

                flight_number_airline_mark = fnc.get("travelProduct.productDetails.identification", segment)
                flight_number_airline_operat = fnc.get("itineraryReservationInfo.reservation.controlNumber", segment)
                control_number = flight_number_airline_mark

                airline_code_marketing = fnc.get("itineraryReservationInfo.reservation.companyId", segment)
                airline_code_operat = fnc.get("travelProduct.companyDetail.identification", segment)

                status = fnc.get("relatedProduct.status", segment)
                if isinstance(status, list):
                    status = status[0]  # we need to recover the first item if status is a list

                segment_reference = fnc.get("elementManagementItinerary.reference.number", segment)
                equipment_type = fnc.get("flightDetail.productDetails.equipment", segment)
                resbook_designator = None
                departure_terminal = fnc.get("flightDetail.departureInformation.departTerminal", segment)
                arrival_terminal = fnc.get("flightDetail.arrivalStationInfo.terminal", segment)

                class_of_servive = fnc.get("travelProduct.productDetails.classOfService", segment)
                action_code = fnc.get("relatedProduct.status", segment)
                number_in_party = fnc.get("relatedProduct.quantity", segment)

                departure = FlightPointDetails(departure_date_time, departure_airport, departure_terminal)
                arrival = FlightPointDetails(arrival_date_time, arrival_airport, arrival_terminal)

                marketing_airline = FlightAirlineDetails(airline_code_marketing, flight_number_airline_mark, None, class_of_servive)
                operating_airline = FlightAirlineDetails(airline_code_operat, flight_number_airline_operat, None, class_of_servive)

                disclosure_carrier = FlightDisclosureCarrier(None, None, None)
                mariage_grp = FlightMarriageGrp(None, None, None)

                seats = None
                segment_data = FlightSegment(
                    segment_reference,
                    resbook_designator,
                    departure_date_time,
                    departure, arrival_date_time,
                    arrival, status,
                    marketing_airline,
                    operating_airline,
                    disclosure_carrier, mariage_grp,
                    seats, action_code, None, None, None, None,
                    None, None, control_number, class_of_servive, None,
                    equipment_type, None, number_in_party, None)

                itinerary_object.addSegment(segment_data)
            all_itineraries.append(itinerary_object)
        return all_itineraries

    def get_gender_by_passenger(self, passenger_id):
        for data in ensure_list(fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])):

            if fnc.get("serviceRequest.ssr.type", data) == "DOCS" and fnc.get(
                    "referenceForDataElement.reference.number", data) == passenger_id:
                free_text = fnc.get("serviceRequest.ssr.freeText", data)
                check_gender = re.split("[, /,////?//:; ]+", free_text) if free_text else None  # to transform the caracter chaine in liste_object

                if check_gender and len(check_gender) >= 3:
                    check_gender = check_gender[2]
                    if check_gender == "M" or check_gender == "F":
                        return check_gender
        return None

    @property
    def get_all_passengers(self):
        all_passengers = []

        for traveller in ensure_list(fnc.get("travellerInfo", self.payload, default=[])):
            reference = fnc.get("elementManagementPassenger.reference.number", traveller)
            name_assoc_id = fnc.get("elementManagementPassenger.reference.number", traveller)
            all_passenger_data = ensure_list(fnc.get("passengerData", traveller, default=[]))
            for index, passenger in enumerate(ensure_list(fnc.get("enhancedPassengerData", traveller, default=[]))):
                date_of_birth_tag = fnc.get("dateOfBirthInEnhancedPaxData.dateAndTimeDetails.date", passenger)

                gender = self.get_gender_by_passenger(reference)
                surname = fnc.get("enhancedTravellerInformation.otherPaxNamesDetails.surname", passenger)
                given_name = fnc.get("enhancedTravellerInformation.otherPaxNamesDetails.givenName", passenger)
                forename = fnc.get("enhancedTravellerInformation.otherPaxNamesDetails.givenName", passenger)
                passenger_type = fnc.get("enhancedTravellerInformation.travellerNameInfo.type", passenger)
                firstname = fnc.get("travellerInformation.passenger.firstName", all_passenger_data[index] if len(all_passenger_data) > index else {})
                last_name = fnc.get("enhancedTravellerInformation.otherPaxNamesDetails.surname", passenger)
                number_in_party = fnc.get("travellerInformation.traveller.quantity", all_passenger_data[index] if len(all_passenger_data) > index else {})

                passsenger_o = Passenger(reference, name_assoc_id, firstname, last_name, date_of_birth_tag, gender, surname, given_name, forename, "",
                                         number_in_party, "", passenger_type, "", {})
                all_passengers.append(passsenger_o)
        return all_passengers

    @property
    def get_dk_number(self):
        for data in ensure_list(
            fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])
        ):
            if "accounting" in data:
                return fnc.get("accounting.account.number", data)
        return None

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

            price_quote_data = PriceQuote_(pq_number, status, fare_type, base_fare, total_fare, tax_fare, validating_carrier, all_passengers, commission_percentage)
            all_price_quote.append(price_quote_data)

        return all_price_quote

    @property
    def get_form_of_payments(self):
        all_form_payment = []
        for data in ensure_list(
            fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])
        ):
            if fnc.get("elementManagementData.segmentName", data) == "FP":
                expire_month = None
                expire_year = None
                card_number = None

                card_type = fnc.get("otherDataFreetext.longFreetext", data)

                if card_type not in ["CASH", "CHECKH"]:
                    two_info = card_type.split(" ")
                    info_cc_exp = two_info[1].split("/") if len(two_info) > 1 else None
                    if info_cc_exp:
                        card_number = info_cc_exp[0][4:] if len(info_cc_exp) > 1 else None
                        expire_year = info_cc_exp[1][2:4] if len(info_cc_exp) > 2 else None
                        expire_month = info_cc_exp[1][:2] if len(info_cc_exp) > 2 else None
                    card_type = "CC"
                form_payment = InfoPaymentCreditCard(card_type=card_type, card_number=card_number, expire_month=expire_month, expire_year=expire_year)
                all_form_payment.append(form_payment)
        return all_form_payment

    def get_passenger(self, name_id):
        for passenger in self.get_all_passengers:
            if passenger.name_id == name_id:
                return passenger

        return None

    def _extract_qualifier_number(self, list_reference):
        list_reference = ensure_list(list_reference)
        for reference in list_reference:
            if reference["qualifier"] == "PT":
                qualifier = reference["qualifier"]
                number = reference["number"]
                return qualifier, number
        return None, None

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
        agent_sign = fnc.get("securityInformation.secondRpInformation.agentSignature", self.payload)
        for ticket in ensure_list(
            fnc.get(
                "dataElementsMaster.dataElementsIndiv", self.payload, default=[]
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
                passenger = self.get_passenger(name_id) if name_id else None

                full_name = (passenger.first_name if passenger.first_name else "") + " " + (passenger.last_name if passenger.last_name else "") if passenger else None
                full_ticket_number = fnc.get(
                    "longFreetext", ticket["otherDataFreetext"] if "otherDataFreetext" in ticket else {}
                )
                index = fnc.get("elementManagementData.reference.number", ticket)

                ticket_number = self.get_ticket_number(full_ticket_number)

                ticketing = TicketingInfo_(
                    ticket_number, transaction_indicator, name_id, agency_location, time_stamp, index, full_ticket_number, agent_sign, full_name
                )

                all_ticket.append(ticketing)
        return all_ticket

    def get_ticket_number(self, ticket_number: str):
        if not ticket_number:
            return ""
        split_value = ticket_number.split(" ")
        value = split_value[len(split_value) - 1]
        return value.split("/")[0]

    @property
    def get_remarks(self):
        all_remark = []
        for data in ensure_list(
            fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])
        ):
            if fnc.get("elementManagementData.segmentName", data) == "RM":
                remark_type = fnc.get("miscellaneousRemarks.remarks.type", data)
                categorie = fnc.get("miscellaneousRemarks.remarks.category", data)
                text = fnc.get("miscellaneousRemarks.remarks.freetext", data)
                index = fnc.get("elementManagementData.reference.number", data)
                remarks_object = Remarks(index, remark_type, categorie, text)
                all_remark.append(remarks_object)
        return all_remark

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

        for ref in ensure_list(fnc.get("referenceForTstData.reference", tst_data, default=[])):
            qualifier, reference = (fnc.get("qualifier", ref), fnc.get("number", ref))
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
        for fe in ensure_list(fnc.get("fareBasisInfo.fareElement", tst_data, default=[])):
            p_code = fnc.get("primaryCode", fe)
            connx = fnc.get("connection", fe)
            n_valid_b = fnc.get("notValidBefore", fe)
            n_valid_b = reformat_date(n_valid_b, "%d%m%y", "%Y-%m-%d") if n_valid_b else None
            n_valid_a = fnc.get("notValidAfter", fe)
            n_valid_a = reformat_date(n_valid_a, "%d%m%y", "%Y-%m-%d") if n_valid_a else None
            b_allow = fnc.get("baggageAllowance", fe)
            f_basis = fnc.get("fareBasis", fe)
            f_el = FareElement(p_code, connx, n_valid_b, n_valid_a, b_allow, f_basis)
            fare_elements.append(f_el)
        return fare_elements

    def _tst_amounts(self, tst_data):
        amounts = []
        base_fare = None
        total_fare = None
        for am in ensure_list(fnc.get("fareData.monetaryInfo", tst_data, default=[])):
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
        for tax_info in ensure_list(fnc.get("fareData.taxFields", tst_data, default=[])):
            tax: TaxInformation = TaxInformation()
            tax.tax_type = fnc.get("taxCountryCode", tax_info)
            tax.tax_nature = fnc.get("taxNatureCode", tax_info)
            am = extract_amount(tax_info, "taxIndicator", "taxAmount", "taxCurrency")
            tax.tax_amount = am
            if not total_taxes_currency:
                total_taxes_currency = am.currency
            if am.currency == total_taxes_currency:  # avoid summing amounts on different currencies
                total_taxes += float(am.amount)
            taxes.append(tax)
        total_taxes = FareAmount(None, total_taxes, total_taxes_currency)
        return total_taxes, taxes
