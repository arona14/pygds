from typing import List
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor, extract_amount
from pygds.core.helpers import ensure_list, get_data_from_xml as from_xml, reformat_date, change_value_if_null
from pygds.core.price import FareElement, TaxInformation, FareAmount
from pygds.core.types import FlightPointDetails, FlightAirlineDetails, FlightSegment, Passenger, Remarks, \
    InfoPaymentCreditCard, FormatAmount, FormatPassengersInPQ, PriceQuote_, TicketingInfo_, Itinerary, FlightDisclosureCarrier, FlightMarriageGrp, InfoPaymentOther
import fnc
from datetime import datetime


class GetPnrResponseExtractor(BaseResponseExtractor):
    """
        A class to extract Reservation from response of retrieve PNR.
    """

    def __init__(self, xml_content: str):
        super().__init__(xml_content, True, True, "PNR_Reply")
        self.parsed = True
        self.payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "PNR_Reply")
        self.all_ssr = {}
        self.all_mariage_group = None

    def _extract(self):
        return {
            'passengers': self.get_all_passengers,
            'itineraries': self._itineraries,
            'form_of_payments': self.get_form_of_payments,
            'price_quotes': self.get_price_quotes,
            'ticketing_info': self.get_ticketing_info,
            'remarks': self.get_remarks,
            'dk_number': self.get_dk_number,
            "record_locator": fnc.get("pnrHeader.reservationInfo.reservation.controlNumber", self.payload),
            "booking_source": fnc.get("securityInformation.secondRpInformation.creationOfficeId", self.payload),
        }

    def segment_book_date(self):
        for data in ensure_list(fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])):
            if fnc.get("miscellaneousRemarks.remarks.category", data) == "B":
                segment_book_date = fnc.get("miscellaneousRemarks.remarks.freetext", data)
                return segment_book_date
        return None

    def get_elapsed_time(self, departure, arrival):
        departure_date = datetime.strptime(departure, "%d%m%y%H%M")
        arrival_date = datetime.strptime(arrival, "%d%m%y%H%M")
        return arrival_date - departure_date

    def get_all_mariage_group(self):
        self.all_mariage_group = {}
        group_id = 1
        for segment_info in ensure_list(fnc.get("segmentGroupingInfo", self.payload, default=())):
            if fnc.get("groupingCode", segment_info) == "MIN":
                for sequence_id, mariage_detail in enumerate(ensure_list(ensure_list(fnc.get("marriageDetail", segment_info, default=[])))):
                    tatoo_number = fnc.get("tatooNum", mariage_detail)
                    if tatoo_number:
                        self.all_mariage_group[tatoo_number] = {
                            "group": str(group_id),
                            "sequence": str(sequence_id + 1),
                            "ind": fnc.get("marriageQualifier", mariage_detail)
                        }
                group_id += 1

    def get_mariage_group_by_segment(self, id_segment):
        if not self.all_mariage_group:
            self.get_all_mariage_group()
        try:
            return self.all_mariage_group[id_segment]
        except Exception:
            return None

    def get_seat_by_segment(self, segment_ref: int):
        for data in ensure_list(fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])):

            if (fnc.get("referenceForDataElement.reference.qualifier", data) == "ST") and (fnc.get(
                    "referenceForDataElement.reference.number", data) == segment_ref):

                is_smoked = False
                return {
                    "id": "",
                    "seat_number": fnc.get("serviceRequest.ssrb.data", data),
                    "smoking_pref_offered_indicator": is_smoked if (fnc.get("serviceRequest.ssrb.seatType", data) == "N") else True,
                    "seat_type_code": fnc.get("serviceRequest.ssrb.seatType", data),
                    "seat_status_code": fnc.get("serviceRequest.ssr.status", data),
                    "name_id": fnc.get("serviceRequest.ssrb.crossRef", data),
                }
        return None

    def get_segment_booked_date(self):

        date_ = fnc.get("pnrHeader.reservationInfo.reservation.date", self.payload)
        time_ = fnc.get("pnrHeader.reservationInfo.reservation.time", self.payload)
        if date_ and time_:
            segment_booked_date = date_ + time_
            return reformat_date(segment_booked_date, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")

    def _get_itinerary(self, itinerary_infos: List):
        itinerary = Itinerary()
        segment_booked_date = self.get_segment_booked_date()
        schedule_change_indicator = "false"
        for segment in itinerary_infos:
            flight_number = fnc.get("travelProduct.productDetails.identification", segment)
            class_of_service = fnc.get("travelProduct.productDetails.classOfService", segment)

            departure_date = fnc.get("travelProduct.product.depDate", segment)
            departure_time = fnc.get("travelProduct.product.depTime", segment)
            departure_date_time = reformat_date(departure_date + departure_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            departure_airport = fnc.get("travelProduct.boardpointDetail.cityCode", segment)
            departure_terminal = fnc.get("flightDetail.departureInformation.departTerminal", segment)
            if departure_terminal is None:
                departure_terminal = ""
            departure = FlightPointDetails(departure_date_time, departure_airport, departure_terminal)

            arrival_date = fnc.get("travelProduct.product.arrDate", segment)
            arrival_time = fnc.get("travelProduct.product.arrTime", segment)
            arrival_date_time = reformat_date(arrival_date + arrival_time, "%d%m%y%H%M", "%Y-%m-%dT%H:%M:%S")
            arrival_airport = fnc.get("travelProduct.offpointDetail.cityCode", segment)
            arrival_terminal = fnc.get("flightDetail.arrivalStationInfo.terminal", segment)
            if arrival_terminal is None:
                arrival_terminal = ""
            arrival = FlightPointDetails(arrival_date_time, arrival_airport, arrival_terminal)

            marketing_airline_code = fnc.get("travelProduct.companyDetail.identification", segment)
            marketing = FlightAirlineDetails(marketing_airline_code, flight_number, "", class_of_service)

            operating_airline_code = marketing_airline_code
            itinerary_free_form_text = fnc.get("itineraryfreeFormText.freeText", segment)
            if itinerary_free_form_text is not None:
                operating_airline_code = str(itinerary_free_form_text).split("BY")[-1].lstrip()
            operating = FlightAirlineDetails(operating_airline_code, flight_number, "", class_of_service)

            segment_reference = fnc.get("elementManagementItinerary.reference.number", segment)
            equipment_type = fnc.get("flightDetail.productDetails.equipment", segment)
            number_of_stop = fnc.get("flightDetail.productDetails.numOfStops", segment)
            resbook_designator = fnc.get("travelProduct.productDetails.classOfService", segment)

            action_code = fnc.get("relatedProduct.status", segment)
            if isinstance(action_code, list) and action_code:
                action_code = action_code[0]
            if action_code != "HK":
                schedule_change_indicator = "true"
            number_in_party = fnc.get("relatedProduct.quantity", segment)

            disclosure_carrier = FlightDisclosureCarrier("", "", "")
            mariage_grp = self.get_mariage_group_by_segment(segment_reference)
            if mariage_grp:
                mariage_grp = FlightMarriageGrp(mariage_grp["ind"], mariage_grp["group"], mariage_grp["sequence"])
            else:
                mariage_grp = FlightMarriageGrp("0", "0", "0")
            elapsed_dep_date_time = departure_date + departure_time
            elapsed_arriv_date_time = arrival_date + arrival_time
            elapsed = self.get_elapsed_time(elapsed_dep_date_time, elapsed_arriv_date_time)
            elapsed = str(elapsed).split(":")
            if len(elapsed[0]) == 1:
                elapsed = "0" + elapsed[0] + "." + elapsed[1]
            else:
                elapsed = elapsed[0] + "." + elapsed[1]
            control_number = fnc.get("itineraryReservationInfo.reservation.controlNumber", segment)
            airline_ref_id = control_number if control_number is not None else fnc.get("pnrHeader.reservationInfo.reservation.controlNumber", self.payload)
            segment_special_request = None
            air_miles_flown = ""
            funnel_flight = "false"
            change_of_gauge = "false"
            eticket = "false"
            type_detail = fnc.get("travelProduct.typeDetail.detail", segment)
            if type_detail is not None and type_detail == "ET":
                eticket = "true"
            seats = self.get_seat_by_segment(segment_reference)
            segment_data = FlightSegment(
                int(segment_reference),
                resbook_designator,
                departure_date_time,
                departure,
                arrival_date_time,
                arrival,
                airline_ref_id,
                marketing,
                operating,
                disclosure_carrier,
                mariage_grp,
                seats,
                action_code,
                segment_special_request,
                schedule_change_indicator,
                segment_booked_date,
                air_miles_flown,
                funnel_flight,
                change_of_gauge,
                flight_number,
                class_of_service,
                elapsed,
                equipment_type,
                eticket,
                number_in_party,
                operating_airline_code,
                number_of_stop)

            itinerary.addSegment(segment_data)
        return itinerary

    @property
    def _itineraries(self):
        list_itineraries = []

        segment_grouping_infos = fnc.get("segmentGroupingInfo", self.payload, default=[])

        if not segment_grouping_infos:
            for itinerary_info in ensure_list(
                    fnc.get("originDestinationDetails.itineraryInfo", self.payload, default=[])):
                list_itineraries.append(
                    self._get_itinerary([itinerary_info])
                )
            return list_itineraries

        for segment in segment_grouping_infos:

            if fnc.get("groupingCode", segment) == "CNX":
                all_segments = [
                    fnc.get("tatooNum", data, default={}) for data in ensure_list(fnc.get("marriageDetail", segment, default=[]))
                ]

                itinerary = []

                for itinerary_info in ensure_list(
                        fnc.get("originDestinationDetails.itineraryInfo", self.payload, default=[])):
                    if fnc.get(
                        "elementManagementItinerary.reference.number", itinerary_info
                    ) in all_segments:
                        itinerary.append(itinerary_info)

                if itinerary:
                    list_itineraries.append(
                        self._get_itinerary(itinerary)
                    )
        return list_itineraries

    def get_seat_by_passenger(self, passenger_id: int):
        for data in ensure_list(fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])):

            if (fnc.get("seatPaxInfo.crossRef.reference.qualifier", data) == "PT") and (fnc.get(
                    "seatPaxInfo.crossRef.reference.number", data) == passenger_id):

                is_smoked = False
                return {
                    "id": "",
                    "seat_number": fnc.get("serviceRequest.ssrb.data", data),
                    "smoking_pref_offered_indicator": is_smoked if (fnc.get("serviceRequest.ssrb.seatType", data) == "N") else True,
                    "seat_type_code": fnc.get("serviceRequest.ssrb.seatType", data),
                    "seat_status_code": fnc.get("serviceRequest.ssr.status", data),
                    "name_id": fnc.get("serviceRequest.ssrb.crossRef", data),
                }
        return None

    def get_all_ssr(self):
        """
        This function is use to get all ssr of type DOCS
        """
        for data in ensure_list(fnc.get("dataElementsMaster.dataElementsIndiv", self.payload, default=[])):
            if (fnc.get("serviceRequest.ssr.type", data) == "DOCS"):
                key = fnc.get("referenceForDataElement.reference.number", data)
                free_text = fnc.get("serviceRequest.ssr.freeText", data)
                ssr = self.get_ssr(free_text) if free_text else []
                gender = ssr[5] if len(ssr) > 5 else None
                if key and gender not in ["MI", "FI"]:
                    self.all_ssr[key] = ssr
                elif key:
                    self.all_ssr[key + "plus"] = ssr

    def get_ssr(self, free_text):
        check_info = free_text.split("/") if free_text else []  # to transform the caracter chaine in liste_object
        return check_info

    def get_ssr_by_passenger(self, passenger_id):

        if not self.all_ssr:
            self.get_all_ssr()
        return fnc.get(passenger_id, self.all_ssr, default=[])

    @property
    def get_all_passengers(self):
        all_passengers = []
        for traveller in ensure_list(fnc.get("travellerInfo", self.payload, default=[])):
            reference = name_assoc_id = fnc.get("elementManagementPassenger.reference.number", traveller)

            for passenger in ensure_list(fnc.get("passengerData", traveller, default=[])):
                seat = self.get_seat_by_passenger(reference)

                number_in_party = fnc.get("travellerInformation.traveller.quantity", passenger)
                last_name = fnc.get("travellerInformation.traveller.surname", passenger)

                info_passengers = ensure_list(fnc.get("travellerInformation.passenger", passenger, default=[]))
                for index, info_passenger in enumerate(info_passengers):
                    firstname = fnc.get("firstName", info_passenger)
                    passenger_type = fnc.get("type", info_passenger)

                    date_of_birth = None
                    reference_p = reference
                    if len(info_passengers) == 1:
                        date_of_birth = fnc.get("dateOfBirth.dateAndTimeDetails.date", passenger)
                    elif index == 1:
                        date_of_birth = fnc.get("dateOfBirth.dateAndTimeDetails.date", passenger)
                        reference_p = reference + "plus" if reference else None

                    if not passenger_type:
                        passenger_type = "ADT"

                    info_ssr = self.get_ssr_by_passenger(reference_p) if reference_p else []
                    gender = info_ssr[5] if len(info_ssr) > 5 else None

                    date_of_birth = change_value_if_null(date_of_birth, info_ssr[4]) if len(info_ssr) > 4 else date_of_birth

                    try:
                        if all([digit.isdigit() for digit in date_of_birth]):
                            date_of_birth = reformat_date(date_of_birth, "%d%m%y", "%m-%d-%Y")
                        else:
                            date_of_birth = reformat_date(date_of_birth, "%d%b%y", "%m-%d-%Y")
                    except Exception:
                        pass

                    last_name = change_value_if_null(last_name, info_ssr[7]) if len(info_ssr) > 7 else last_name
                    firstname = change_value_if_null(firstname, info_ssr[8]) if len(info_ssr) > 8 else firstname
                    middle_name = ""

                    passsenger_o = Passenger(reference, name_assoc_id, firstname, last_name, date_of_birth, gender, "", "", middle_name,
                                             "", number_in_party, "", passenger_type, "", seat)
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
    def get_agent_sine(self):
        return fnc.get("securityInformation.secondRpInformation.agentSignature", self.payload, default="")

    @property
    def get_price_quotes(self):
        all_price_quote = []

        for tst in self._tst_data():
            all_passengers = []

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

            for passenger in tst["passenger_references"]:
                passenger = FormatPassengersInPQ(
                    passenger["name_id"] if "name_id" in passenger else None, passenger["type"] if "type" in passenger else None
                ).to_data()
                all_passengers.append(passenger)

            pq_number = tst["tst_reference_number"]

            validating_carrier = tst["validating_carrier"]

            status = tst["status"]

            fare_type = None

            commission_percentage = tst["commission"]

            price_quote_data = PriceQuote_(
                pq_number, status, fare_type, base_fare, total_fare, tax_fare, validating_carrier, all_passengers, commission_percentage)
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
                conditions = [
                    "CASH" not in card_type, "CHECK" not in card_type
                ]
                if all(conditions):
                    two_info = card_type.split(" ") if " " in card_type else card_type
                    info_cc_exp = two_info[1].split("/") if isinstance(two_info, list) else two_info.split("/")
                    if info_cc_exp:
                        card_number = "".join([i for i in info_cc_exp[0] if (i.isdigit() or i == "X")]) if len(info_cc_exp) > 0 else None
                        expire_year = info_cc_exp[1][2:4] if len(info_cc_exp) > 1 else None
                        expire_month = info_cc_exp[1][:2] if len(info_cc_exp) > 1 else None
                    card_type = "CC"
                    form_payment = InfoPaymentCreditCard(card_type=card_type, card_number=card_number, expire_month=expire_month, expire_year=expire_year)
                else:
                    form_payment = InfoPaymentOther(card_type)
                all_form_payment.append(form_payment)
        return all_form_payment

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
        list_ticket = []
        for ticket in ensure_list(
            fnc.get(
                "dataElementsIndiv", fnc.get("dataElementsMaster", self.payload, default={}), default=[]
            )
        ):
            if "ticketElement" in ticket:
                agency_location = fnc.get("ticketElement.ticket.officeId", ticket)
                ticket_date = fnc.get("ticketElement.ticket.date", ticket)
                if fnc.get("ticketElement.ticket.time", ticket) is not None:
                    ticket_date = ticket_date + "T" + fnc.get("ticketElement.ticket.time", ticket)
                    ticket_date_format = reformat_date(ticket_date, "%d%m%yT%H%M", "%Y-%m-%dT%H:%M")
                    time_stamp = reformat_date(ticket_date, "%d%m%yT%H%M", "%H%M/%d%b")
                else:
                    ticket_date_format = reformat_date(ticket_date, "%d%m%y", "%Y-%m-%d")
                    time_stamp = reformat_date(ticket_date, "%d%m%y", "%d%b")

                transaction_indicator = fnc.get("ticketElement.ticket.indicator", ticket)

            if fnc.get("elementManagementData.segmentName", ticket) in ["FA"]:
                list_reference = fnc.get(
                    "reference", ticket["referenceForDataElement"] if "referenceForDataElement" in ticket else {}
                )
                full_ticket_number = fnc.get(
                    "longFreetext", ticket["otherDataFreetext"] if "otherDataFreetext" in ticket else {}
                )
                index = fnc.get("elementManagementData.reference.number", ticket)

                ticket_number = self.get_ticket_number(full_ticket_number)
                ticket_number = ticket_number.replace("-", "")
                passenger_type = None
                if "PAX" not in full_ticket_number:
                    passenger_type = "INF"

                agent_sine = self.get_agent_sine
                qualifier, name_id = self._extract_qualifier_number(list_reference)
                passenger = self.get_passenger(name_id, passenger_type)

                full_name = (passenger.first_name if passenger.first_name else "") + " " + (passenger.last_name if passenger.last_name else "") if passenger else None

                original_ticket_detail = f"{transaction_indicator} {ticket_number}-AT {passenger.last_name}/{passenger.first_name[0]} {agency_location}*{agent_sine} {time_stamp}"

                ticket_object = TicketingInfo_(
                    ticket_number, transaction_indicator, name_id, agency_location, ticket_date_format, index, original_ticket_detail, agent_sine, full_name
                )
                list_ticket.append(ticket_object)
        return list_ticket

    def get_passenger(self, name_id, passenger_type):
        for passenger in self.get_all_passengers:

            if all([passenger.name_id == name_id, passenger_type == "INF", passenger.passenger_type == "INF"]):
                return passenger
            elif passenger.name_id == name_id:
                return passenger

        return None

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
            tst_reference_number = fnc.get(
                "tstGeneralInformation.generalInformation.tstReferenceNumber", tst_data
            )
            passenger_type = None
            commission = None
            status = None
            validating_carrier = None
            for free_text in ensure_list(fnc.get("tstFreetext", tst_data)):
                if fnc.get("freetextDetail.type", free_text) == "41":
                    passenger_type = fnc.get("longFreetext", free_text)
                if fnc.get("freetextDetail.type", free_text) == "11":
                    commission = fnc.get("longFreetext", free_text)
                if fnc.get("freetextDetail.type", free_text) == "17":
                    status = fnc.get("longFreetext", free_text)
                if fnc.get("freetextDetail.type", free_text) == "P18":
                    validating_carrier = fnc.get("longFreetext", free_text)
            fare_type = "PUB"
            for option in ensure_list(fnc.get("segmentAssociation.selection", tst_data)):
                if fnc.get("option", option) == "B":
                    fare_type = "NET"

            fare_elements = self._tst_fare_elements(tst_data)
            total_taxes, taxes = self._tst_taxes(tst_data)
            pax_refs, segment_refs = self._tst_pax_segs_refs(tst_data, passenger_type)
            base_fare, total_fare, amounts = self._tst_amounts(tst_data)

            tst = {
                "fare_type": fare_type,
                "status": status,
                "validating_carrier": validating_carrier,
                "commission": commission,
                "tst_reference_number": tst_reference_number,
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

    def _tst_pax_segs_refs(self, tst_data, passenger_type):
        pax_refs = []
        segment_refs = []
        passengers = self.get_all_passengers
        if passenger_type == "INF":
            passengers = [passenger for passenger in passengers if passenger.passenger_type == "INF"]
        else:
            passengers = [passenger for passenger in passengers if passenger.passenger_type != "INF"]

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
        total_taxes = FareAmount(None, round(total_taxes, 2), total_taxes_currency)
        return total_taxes, taxes
