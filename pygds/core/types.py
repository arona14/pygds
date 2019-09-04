from typing import List
import json
import datetime


class BasicDataObject(object):
    """
        A basic class that contains data.
    """

    def to_data(self):
        """
            Method that returns a dictionary containing useful data. Must be implemented by sub-classes
        """
        raise NotImplementedError(" this is not yet implemented")

    def to_json(self):
        """
            Dumps the object to json string
        """
        return json.dumps(self.to_data(), indent=4)

    def __repr__(self):
        """
            method that redefined the string type
        """
        return self.to_json()


class FlightPointDetails(BasicDataObject):
    """
        Information about flight point details (on departure or arrival)
    """

    def __init__(self, departure_date_time: str = None, airport: str = None, terminal: str = None):
        self.airport = airport
        self.departure_date_time = departure_date_time
        self.terminal = terminal

    def to_data(self):
        return {
            "airport_code": self.airport,
            "departure_date_time": self.departure_date_time,
            "terminal": self.terminal
        }


class FlightAirlineDetails(BasicDataObject):
    """
        Holds informations about airline
    """

    def __init__(self, airline_code: str = None, flight_number: str = None, airline_short_name: str = None, class_of_service: str = None):
        self.airline_code = airline_code
        self.flight_number = flight_number
        self.airline_short_name = airline_short_name
        self.class_of_service = class_of_service

    def to_data(self):
        return{
            "airline_code": self.airline_code,
            "flight_number": self.flight_number,
            "airline_short_name": self.airline_short_name,
            "class_of_service": self.class_of_service
        }


class FlightDisclosureCarrier(BasicDataObject):
    def __init__(self, code: str = None, dot: str = None, banner: str = None):
        self.code = code
        self.dot = dot
        self.banner = banner

    def to_data(self):
        return{
            "code": self.code,
            "dot": self.dot,
            "banner": self.banner
        }


class FlightMarriageGrp(BasicDataObject):
    """
    Holds information of MariageGroup
    """

    def __init__(self, ind: str = None, group: str = None, sequence: str = None):
        self.ind = ind
        self.group = group
        self.sequence = sequence

    def to_data(self):
        return{
            "ind": self.ind,
            "group": self.group,
            "sequence": self.sequence
        }


class FlightSegment(BasicDataObject):
    """
        Holds information about a segment
    """
    def __init__(self, sequence: int = 1, res_book_desig_code: str = None, departure_date_time: str = None, departure_airport: FlightPointDetails = None, arrival_date_time: str = None, arrival_airpot: FlightPointDetails = None, airline: str = None, marketing: FlightAirlineDetails = None, operating: FlightAirlineDetails = None, disclosure_carrier: FlightDisclosureCarrier = None, mariage_group: FlightMarriageGrp = None, seats: str = None, action_code: str = None, segment_special_requests: str = None, schedule_change_indicator: str = None, segment_booked_date: str = None, air_miles_flown: str = None, funnel_flight: str = None, change_of_gauge: str = None, flight_number: str = None, class_of_service: str = None, elapsed_time: str = None, equipment_type: str = None, eticket: str = None, number_in_party: str = None, code: str = None, status: str = None):
        self.sequence = sequence
        self.res_book_desig_code = res_book_desig_code
        self.departure_date_time = departure_date_time
        self.departure_airport = departure_airport
        self.arrival_date_time = arrival_date_time
        self.arrival_airpot = arrival_airpot
        self.airline = airline
        self.marketing = marketing
        self.operating = operating
        self.disclosure_carrier = disclosure_carrier
        self.mariage_group = mariage_group
        self.seats = seats
        self.segment_special_requests = segment_special_requests
        self.schedule_change_indicator = schedule_change_indicator
        self.segment_booked_date = segment_booked_date
        self.air_miles_flown = air_miles_flown
        self.funnel_flight = funnel_flight
        self.change_of_gauge = change_of_gauge
        self.flight_number = flight_number
        self.class_of_service = class_of_service
        self.elapsed_time = elapsed_time
        self.equipment_type = equipment_type
        self.eticket = eticket
        self.number_in_party = number_in_party
        self.code = code
        self.action_code = action_code
        self.status = status

    def to_data(self):
        return {
            "sequence": self.sequence,
            "res_book_desig_code": self.res_book_desig_code,
            "departure": self.departure_airport.to_data() if self.departure_airport else None,
            "arrival": self.arrival_airpot.to_data() if self.arrival_airpot else None,
            "airline_ref_id": self.airline,
            "marketing": self.marketing.to_data() if self.marketing else None,
            "operating": self.operating.to_data() if self.operating else None,
            "disclosure_carrier": self.disclosure_carrier.to_data() if self.disclosure_carrier else None,
            "mariage_group": self.mariage_group.to_data() if self.mariage_group else None,
            "seats": self.seats,
            "segment_special_requests": self.segment_special_requests,
            "schedule_change_indicator": self.schedule_change_indicator,
            "segment_booked_date": self.segment_booked_date,
            "air_miles_flown": self.air_miles_flown,
            "funnel_flight": self.funnel_flight,
            "change_of_gauge": self.change_of_gauge,
            "flight_number": self.flight_number,
            "class_of_service": self.class_of_service,
            "elapsed_time": self.elapsed_time,
            "equipment_type": self.equipment_type,
            "eticket": self.eticket,
            "number_in_party": self.number_in_party,
            "code": self.code,
            "action_code": self.action_code,

        }


class Itinerary(BasicDataObject):

    """
        Holds information about an itinerary
    """

    def __init__(self, itinerary_type: str = None, elapsed_time: str = None):

        self.segments: List[FlightSegment] = []
        self.itinerary_type = itinerary_type
        self.elapsed_time = elapsed_time

    def addSegment(self, segment: FlightSegment):
        """
            Adds a new segment to an itinerary
        """
        self.segments.append(segment)
        return self

    def to_data(self):
        return {
            # "code": self.code,
            # "resBookDesigCode": self.res_book_desig_code,
            # "departureAirport": self.departure_airport,
            # "arrivalAirport": self.arrival_airport,
            # "operatingAirlineCode": self.operating_airline_code,
            # "marketingAirlineCode": self.marketing_airline_code,
            # "equipmentType": self.equipment_type,
            # "eticket": self.eticket,
            # "departureDateTime": self.departure_date_time,
            # "arrivalDateTime": self.arrival_date_time,
            # "flightNumber": self.flight_number,
            # "classOfService": self.class_of_service,
            # "numberInParty": self.number_in_party,
            # "onBoundConnection": self.out_bound_connection,
            # "inBoundConnection": self.in_bound_connection,
            # "airlineRefId": self.air_line_ref_id,
            # "elapsedTime": self.elapsed_time,
            "segments": [s.to_data() for s in self.segments],
            "itineraryType": self.itinerary_type,
            "elapsed_time": self.elapsed_time
        }


class PassengerPreferences(BasicDataObject):
    """
        This is for holding preferences of a passenger
    """

    def __init__(self, prefs: dict = {}):
        self.prefs = prefs

    def to_data(self):
        return self.prefs


class Passenger(BasicDataObject):
    """
        A class to keep information about a passenger
    """

    def __init__(self, name_id: str = None, first_name: str = None, last_name: str = None, date_of_birth: str = None, gender: str = None, sur_name: str = None, fore_name: str = None, middle_name: str = None, action_code: str = None, number_in_party: str = None, vendor_code: str = None, passenger_type: str = None, preferences=None):
        self.name_id = name_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.sur_name = sur_name
        self.fore_name = fore_name
        self.middle_name = middle_name
        self.action_code = action_code
        self.number_in_party = number_in_party
        self.vendor_code = vendor_code
        self.passenger_type = passenger_type
        self.preferences = preferences if isinstance(preferences, PassengerPreferences) else PassengerPreferences(preferences) if isinstance(preferences, dict) else PassengerPreferences({})
        # self.retrieve_passenger_type()

    def retrieve_passenger_type(self):
        """
            This method retrieves the passenger type from the age
        """
        if self.date_of_birth is not None:
            age = datetime.date.today() - datetime.date.fromisoformat(self.date_of_birth)
            age = age.days / 365
            if age < 0:
                self.passenger_type = None
            elif age <= 2:
                self.passenger_type = "INF"
            elif age <= 12:
                self.passenger_type = "CNN"
            else:
                self.passenger_type = "ADT"

    def to_data(self):
        return {
            "name_id": self.name_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "number_in_party": self.number_in_party,
            "passenger_type": self.passenger_type,
            "preferences": self.preferences.to_data()
        }


class FormOfPayment(BasicDataObject):
    """
        Keeps information about form of payments
    """

    def __init__(self, type_payment: str = None, form_payment: str = None, vendor_code: str = None,
                 credit_card_number: str = None, expire_date: str = None):
        self.type_payment = type_payment
        self.form_payment = form_payment
        self.vendor_code = vendor_code
        self.credit_card_number = credit_card_number
        self.expire_date = expire_date

    def to_data(self):
        return {
            "type_payment": self.type_payment,
            "form_payment": self.form_payment,
            "vendor_code": self.vendor_code,
            "credit_card_number": self.credit_card_number,
            "expire_date": self.expire_date
        }


class FlightPriceQuote(BasicDataObject):
    """[summary]
    Arguments:
        BasicDataObject {[type]} -- [description]
    """

    def __init__(self, latest_pq_flag: str = None, number: str = None, pricing_type: str = None, status: str = None, type_pq: str = None, itinerary_type: str = None, validating_carrier: str = None, local_create_date_time: str = None):
        self.latest_pq_flag = latest_pq_flag
        self.number = number
        self.pricing_type = pricing_type
        self.status = status
        self.type_pq = type_pq
        self.itinerary_type = itinerary_type
        self.validating_carrier = validating_carrier
        self.local_create_date_time = local_create_date_time

    def to_data(self):
        return{
            "latest_pq_flag": self.latest_pq_flag,
            "number": self.number,
            "pricing_type": self.pricing_type,
            "status": self.status,
            "type_pq": self.type_pq,
            "itinerary_type": self.itinerary_type,
            "validating_carrier": self.validating_carrier,
            "local_create_date_time": self.local_create_date_time
        }


class FlightAmounts(BasicDataObject):
    """[summary]

    Arguments:
        BasicDataObject {[type]} -- [description]
    """

    def __init__(self, currency_code: str = None, decimal_place: str = None, text: str = None):
        self.currency_code = currency_code
        self.decimal_place = decimal_place
        self.text = text

    def to_data(self):
        return{
            "currency_code": self.currency_code,
            "decimal_place": self.decimal_place,
            "amounts": self.text
        }


class FlightPassenger_pq(BasicDataObject):
    """[summary]
    Arguments:
        BasicDataObject {[type]} -- [description]
    """

    def __init__(self, passenger_type_count: str = None, requested_type: str = None, type_passenger: str = None):
        self.passenger_type_count = passenger_type_count
        self.requested_type = requested_type
        self.type_passenger = type_passenger

    def to_data(self):
        return{
            "passenger_type_count": self.passenger_type_count,
            "request_type": self.requested_type,
            "type_passenger": self.type_passenger
        }


class FlightSummary(BasicDataObject):
    """
    Holds informations Nameassociation for passengers
    """

    def __init__(self, first_name: str = None, last_name: str = None, name_id: str = None, name_number: str = None, pq: FlightPriceQuote = None, passenger: FlightPassenger_pq = None, amounts: FlightAmounts = None):
        self.first_name = first_name
        self.last_name = last_name
        self.name_id = name_id
        self.name_number = name_number
        self.pq = pq
        self.passenger = passenger
        self.amounts = amounts

    def to_data(self):
        return{
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name_id": self.name_id,
            "name_number": self.name_number,
            "price_quote": None if self.pq is None else self.pq.to_data(),
            "passenger": None if self.passenger is None else self.passenger.to_data(),
            "amounts": None if self.amounts is None else self.amounts.to_data()
        }


class PriceQuote(BasicDataObject):
    """
        This is to represent a price quote object
    """

    def __init__(self, summary: FlightSummary = None):
        self.summary = summary

    def to_data(self):
        return{
            "summary": None if self.summary is None else self.summary.to_data()
        }


class FormatAmount(BasicDataObject):

    def __init__(self, amount: str = None, currency_code: str = None):
        self.amount = amount
        self.currency_code = currency_code

    def to_data(self):
        return{
            "amount": self.amount,
            "currency_code": self.currency_code,
        }


class FormatPassengersInPQ(BasicDataObject):

    def __init__(self, name_number: str = None, passenger_type: str = None):
        self.name_number = name_number
        self.passenger_type = passenger_type

    def to_data(self):
        return{
            "name_number": self.name_number,
            "passenger_type": self.passenger_type,

        }


class PriceQuote_(BasicDataObject):
    """
        This is to represent a price quote object
    """

    def __init__(self, pq_number: int = None, status: str = None, fare_type: str = None, base_fare=None, total_fare=None, total_tax=None, passengers=None):
        self.price_quote_number = pq_number
        self.status = status
        self.fare_type = fare_type
        self.base_fare = base_fare
        self.total_fare = total_fare
        self.total_tax = total_tax
        self.passengers = passengers

    def to_data(self):
        return{
            "price_quote_number": self.price_quote_number,
            "status": self.status,
            "fare_type": self.fare_type,
            "base_fare": self.base_fare,
            "total_fare": self.total_fare,
            "total_tax": self.total_tax,
            "passengers": self.passengers,

        }


class TicketingInfo(BasicDataObject):
    """
        Represents a ticketing information
    """

    def __init__(self, id: str = None, index: str = None, element_id: str = None, code: str = None,
                 branch_pcc: str = None, date: str = None, time: str = None, queue_number: str = None,
                 comment: str = None, long_free_text: str = None, qualifier: str = None,
                 number: str = None):
        self.id = id
        self.index = index
        self.element_id = element_id
        self.code = code
        self.branch_pcc = branch_pcc
        self.date = date
        self.time = time
        self.queue_number = queue_number
        self.comment = comment
        self.long_free_text = long_free_text
        self.qualifier = qualifier
        self.number = number

    def to_data(self):
        return {
            "id": self.id,
            "index": self.index,
            "element_id": self.element_id,
            "code": self.code,
            "branch_pcc": self.branch_pcc,
            "date": self.date,
            "time": self.time,
            "queue_number": self.queue_number,
            "comment": self.comment,
            "number": self.number,
            "qualifier": self.qualifier,
            "long_free_text": self.long_free_text
        }


class TicketingInfo_(BasicDataObject):
    """
        Represents a ticketing information
    """

    def __init__(self, ticket_number: str = None, transaction_indicator: str = None, passenger: str = None, pcc: str = None, date_time: str = None):
        self.ticket_number = ticket_number
        self.transaction_indicator = transaction_indicator
        self.passenger = passenger
        self.pcc = pcc
        self.date_time = date_time

    def to_data(self):
        return{
            "ticket_number": self.ticket_number,
            "transaction_indicator": self.transaction_indicator,
            "passenger_name": self.passenger,
            "agency_location": self.pcc,
            "time_stamp": self.date_time,
        }


class PnrInfo(BasicDataObject):
    """
    This class keep all informations of pnr
    """

    def __init__(self, dk_number: str = None, agent_signature: str = None, creation_office_id: str = None, creation_date: str = None):
        self.dk_number = dk_number
        self.agent_signature = agent_signature
        self.creation_office_id = creation_office_id
        self.creation_date = creation_date

    def to_data(self):
        return {
            "dk_number": self.dk_number,
            "agent_signature": self.agent_signature,
            "creation_office_id": self.creation_office_id,
            "creation_date": self.creation_date
        }


class Remarks(BasicDataObject):
    """
     feep informations about remarks
    """

    def __init__(self, sequence: int = 1, type_remark: str = None, element_id: str = None, text: str = None):
        self.sequence = sequence
        self.type_remark = type_remark
        self.element_id = element_id
        self.text = text

    def to_data(self):
        return{
            "sequence": self.sequence,
            "type_remark": self.type_remark,
            "element_id": self.element_id,
            "text": self.text
        }


class FareElement(BasicDataObject):

    def __init__(self, primary_code, connection, not_valid_before, not_valid_after, baggage_allowance, fare_basis):
        self.primary_code = primary_code
        self.connection = connection
        self.not_valid_before = not_valid_before
        self.not_valid_after = not_valid_after
        self.baggage_allowance = baggage_allowance
        self.fare_basis = fare_basis

    def to_dict(self):
        return {
            "primary_code": self.primary_code,
            "connection": self.connection,
            "not_valid_before": self.not_valid_before,
            "not_valid_after": self.not_valid_after,
            "baggage_allowance": self.baggage_allowance,
            "fare_basis": self.fare_basis
        }


class Reservation(BasicDataObject):
    """
        A class to keep all data about reservation
    """

    def __init__(self):
        self.itinerary: List[Itinerary] = []
        self.passengers: List[Passenger] = []
        self.formOfPayments: List[FormOfPayment] = []
        self.priceQuotes: List[PriceQuote] = []
        self.ticketingInfo: TicketingInfo = None

    def addItinerary(self, itnr: Itinerary):
        """
            Add a new itinerary to the reservation
        """
        self.itinerary.append(itnr)
        return self

    def addPassenger(self, psgr: Passenger):
        """
            Adding passenger to the reservation
        """
        self.passengers.append(psgr)
        return self

    def addFormOfPayment(self, fp: FormOfPayment):
        """
            Add a form of payment to the reservation
        """
        self.formOfPayments.append(fp)
        return self

    def to_data(self):
        return {
            "itineraries": [],
            "passengers": [p.to_data() for p in self.passengers],
            "formOfPayments": [f.to_data() for f in self.formOfPayments],
            "priceQuotes": [p.to_data() for p in self.priceQuotes],
            "ticketingInfo": self.ticketingInfo.to_data() if self.ticketingInfo is not None else {}
        }


class SellItinerary(BasicDataObject):

    def __init__(self, origin, destination, departure_date, company, flight_number, booking_class, quantity):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.company = company
        self.flight_number = flight_number
        self.booking_class = booking_class
        self.quantity = quantity


class TravellerInfo(BasicDataObject):
    def to_data(self):
        pass

    def __init__(self, ref_number, first_name, surname, last_name, date_of_birth, pax_type):
        self.ref_number = ref_number
        self.first_name = first_name
        self.surname = surname
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.pax_type = pax_type


class TravellerNumbering(BasicDataObject):
    """
        This class is for holding information about the numbering of traveller.
    """

    def to_data(self):
        return {"adults": self.adults, "children": self.children, "infants": self.infants}

    def __init__(self, adults: int, children: int = 0, infants: int = 0):
        self.adults = adults
        self.children = children
        self.infants = infants

    """ Gives the total number of traveller"""

    def total_travellers(self):
        return self.adults + self.children + self.infants

    """ Gives the total number of seats to occupy"""

    def total_seats(self):
        return self.adults + self.children


class SendCommand(BasicDataObject):
    """
        This is to represent a send command object
    """

    def __init__(self, response: str = None):
        self.response = response

    def to_data(self):
        return{
            "response": self.response,
        }


class EndTransaction():
    """This class is for holding information about end transaction
    """

    def __init__(self, status: str = None, id_ref: str = None, create_date_time: str = None, text_message: str = None):
        self.status = status
        self.id_ref = id_ref
        self.create_date_time = create_date_time
        self.text_message = text_message

    def to_data(self):
        return {"status": self.status, "id_ref": self.id_ref, "create_date_time": self.create_date_time, "text_message": self.text_message}


class QueuePlace():
    """This class is for holding information about queue place
    """

    def __init__(self, status: str = None, type_response: str = None, text_message: str = None):
        self.status = status
        self.type_response = type_response
        self.text_message = text_message

    def to_data(self):
        return {"status": self.status, "type_response": self.type_response, "text_message": self.text_message}


class IgnoreTransaction():
    """This class is for holding information about ignore transaction
    """

    def __init__(self, status: str = None, create_date_time: str = None):
        self.status = status
        self.create_date_time = create_date_time

    def to_data(self):
        return {"status": self.status, "create_date_time": self.create_date_time}


class Agent(BasicDataObject):

    def __init__(self, sine: str = None, ticketing_provider: str = None, work_location: str = None, home_location: str = None, iso_country_code: str = None):
        self.sine = sine
        self.ticketing_provider = ticketing_provider
        self.work_location = work_location
        self.home_location = home_location
        self.iso_country_code = iso_country_code

    def to_data(self):
        return {
            "sine": self.sine,
            "ticketing_provider": self.ticketing_provider,
            "Work_location": self.work_location,
            "home_location": self.home_location,
            "iso_country_code": self.iso_country_code
        }


class ServiceCoupon(BasicDataObject):

    def __init__(self, coupon: int = None, marketing_provider: str = None, marketing_flight_number: str = None, operating_provider: str = None, origin: str = None, destination: str = None, class_of_service: str = None, booking_status: str = None, current_status: str = None):

        self.coupon = coupon
        self.marketing_provider = marketing_provider
        self.marketing_flight_number = marketing_flight_number
        self.operating_provider = operating_provider
        self.origin = origin
        self.destination = destination
        self.class_of_service = class_of_service
        self.booking_status = booking_status
        self.current_status = current_status

    def to_data(self):
        return {
            "coupon": self.coupon,
            "marketing_provider": self.marketing_provider,
            "marketing_flight_number": self.marketing_flight_number,
            "operating_provider": self.operating_provider,
            "origin": self.origin,
            "destination": self.destination,
            "class_of_service": self.class_of_service,
            "booking_status": self.booking_status,
            "current_status": self.current_status
        }


class TicketDetails(BasicDataObject):

    def __init__(self, number: str = None, traveler: str = None):
        self.number = number
        self.traveler = traveler
        self.service_coupon: List[ServiceCoupon] = []

    def add_service_coupon(self, coupon: ServiceCoupon):

        self.service_coupon.append(coupon)
        return self

    def to_data(self):
        return {
            "number": self.number,
            "traveler": self.traveler,
            "service_coupon": [s.to_data() for s in self.service_coupon],

        }


class ElectronicDocument(BasicDataObject):
    """
        Holds information about a segment
    """
    def __init__(self, status: str = None, agent: Agent = None, ticket_details: TicketDetails = None):
        self.status = status
        self.agent = agent
        self.ticket_details = ticket_details

    def to_data(self):
        return {
            "status": self.status,
            "agent": self.agent.to_data() if self.agent else None,
            "ticket_details": self.ticket_details.to_data() if self.ticket_details else None
        }


class OperatingMarketing(BasicDataObject):
    """This class is for holding information about Operating and Marketing Code
    """

    def __init__(self, carrier: str = None, code: str = None):
        self.carrier = carrier
        self.code = code

    def to_data(self):
        return {"carrier": self.carrier, "#text": self.code}


class FlightInfo(BasicDataObject):
    """This class is for holding information about the flight
    """

    def __init__(self, destination: str = None, origin: str = None, Departure_date: str = None, operating: OperatingMarketing = None, marketing: OperatingMarketing = None):
        self.destination = destination
        self.origin = origin
        self.departure_date = Departure_date
        self.operating = operating
        self.marketing = marketing

    def to_data(self):
        return {
            "destination": self.destination,
            "origin": self.origin,
            "DepartureDate": self.departure_date,
            "Operating": self.operating.to_data() if self.operating is not None else None,
            "Marketing": self.marketing.to_data() if self.marketing is not None else None
        }


class CabinClass(BasicDataObject):
    """This class is for holding information about the cabin class
    """

    def __init__(self, class_of_service: str = None, marketing_description: str = None):
        self.class_of_service = class_of_service
        self.marketing_description = marketing_description

    def to_data(self):
        return {"RBD": self.class_of_service, "MarketingDescription": self.marketing_description}


class TotalAmount(BasicDataObject):
    """This class is for holding information about the total amount
    """

    def __init__(self, currency_code: str = None, text: str = None):
        self.currency_code = currency_code
        self.text = text

    def to_data(self):
        return {"currencyCode": self.currency_code, "#text": self.text}


class Occupation(BasicDataObject):
    """This class is for holding information about the Occupation
    """

    def __init__(self, detail: str = None):
        self.detail = detail

    def to_data(self):
        return {"Detail": self.detail}


class Facilities(BasicDataObject):
    """This class is for holding information about the Facilities
    """

    def __init__(self, detail: str = None):
        self.detail = detail

    def to_data(self):
        return {"Detail": self.detail}


class BasePrice(BasicDataObject):
    """This class is for holding information about the base price
    """

    def __init__(self, total_amount: TotalAmount = None):
        self.total_amount = total_amount

    def to_data(self):
        return {"TotalAmount": self.total_amount.to_data() if self.total_amount is not None else {}}


class Offer(BasicDataObject):
    """This class is for holding information about the Offer
    """

    def __init__(self, entitle_ind: str = None, commercial_name: str = None, base_price: BasePrice = None):
        self.entitle_ind = entitle_ind
        self.commercial_name = commercial_name
        self.base_price = base_price

    def to_data(self):
        return {
            "entitledInd": self.entitle_ind,
            "CommercialName": self.commercial_name,
            "BasePrice": self.base_price.to_data() if self.base_price is not None else {}
        }


class SeatInfo(BasicDataObject):
    """This class is for holding information about the flight
    """

    def __init__(self, occupied_ind: str = None, inoperative_ind: str = None, premiun_ind: str = None, chargeable_ind: str = None, exit_row_ind: str = None, restricted_reclined_ind: str = None, no_enfant_ind: str = None, number: str = None, occupation: Occupation = None, facilities: Facilities = None, offer: Offer = None):
        self.occupied_ind = occupied_ind
        self.inoperative_ind = inoperative_ind
        self.premiun_ind = premiun_ind
        self.chargeable_ind = chargeable_ind
        self.exit_row_ind = exit_row_ind
        self.restricted_reclined_ind = restricted_reclined_ind
        self.no_enfant_ind = no_enfant_ind
        self.number = number
        self.occupation = occupation
        self.facilities = facilities
        self.offer = offer

    def to_data(self):
        return {
            "occupiedInd": self.occupied_ind,
            "inoperativeInd": self.inoperative_ind,
            "premiumInd": self.premiun_ind,
            "chargeableInd": self.chargeable_ind,
            "exitRowInd": self.exit_row_ind,
            "restrictedReclineInd": self.restricted_reclined_ind,
            "noInfantInd": self.no_enfant_ind,
            "Number": self.number,
            "Occupation": self.occupation.to_data() if self.occupation is not None else None,
            "Facilities": [self.facilities.to_data() if self.facilities is not None else None],
            "Offer": self.offer.to_data() if self.offer is not None else None
        }


class RowInfo(BasicDataObject):
    """This class is for holding information about the cabin class
    """

    def __init__(self, row_number: str = None, seat_info: SeatInfo = None):
        self.row_number = row_number
        self.seat_info = seat_info

    def to_data(self):
        return {"RowNumber": self.row_number, "Seat": [self.seat_info.to_data() if self.seat_info is not None else None]}


class ColumnInfo(BasicDataObject):
    """This class is for holding information about the cabin class
    """

    def __init__(self, column: str = None, caracteristics: str = None):
        self.column = column
        self.caracteristics = caracteristics

    def to_data(self):
        return {"Column": self.column, "Characteristics": self.caracteristics}


class CabinInfo(BasicDataObject):
    """This class is for holding information about the Cabin Info
    """

    def __init__(self, first_raw: str = None, last_raw: str = None, cabin_class: CabinClass = None, row: RowInfo = None, column: ColumnInfo = None):
        self.first_raw = first_raw
        self.last_raw = last_raw
        self.cabin_class = cabin_class
        self.row = row
        self.column = column

    def to_data(self):
        return {
            "firstRow": self.first_raw,
            "lastRow": self.last_raw,
            "CabinClass": self.cabin_class,
            "Row": [self.row.to_data() if self.row is not None else None],
            "Column": [self.column.to_data() if self.column is not None else None]
        }


class SeatMap(BasicDataObject):

    """This class is for holding information about seat map
    """

    def __init__(self, change_of_gauge_ind: str = None, equipement: str = None, flights: FlightInfo = None, cabin: CabinInfo = None):
        self.change_of_gauge_ind = change_of_gauge_ind
        self.equipement = equipement
        self.flights = flights
        self.cabin = cabin

    def to_data(self):
        return {
            "changeOfGaugeInd": self.change_of_gauge_ind,
            "Equipement": self.equipement,
            "Flight": self.flights if self.flights is not None else None,
            "Cabin": self.cabin if self.cabin is not None else None
        }


class PassengerUpdate:
    def __init__(self):
        self.name_number: str = None
        self.dk_number: str = None
        self.date_of_birth: str = None
        self.gender: str = None
        self.first_name: str = None
        self.last_name: str = None
        self.segment_number: str = None
        self.ssr_code: str = None
        self.seat_number: str = None
