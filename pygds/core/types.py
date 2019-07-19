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
    def __init__(self, content: str = None, airport: str = None, terminal: str = None):
        self.content = content
        self.airport = airport
        self.terminal = terminal

    def to_data(self):
        return {
            "content": self.content,
            "location_code": self.airport,
            "terminal": self.terminal
        }


class FlightAirlineDetails():
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
    def __init__(self, sequence: int = 1, res_book_desig_code: str = None, departure_date_time: str = None, departure_airport: FlightPointDetails = None, arrival_date_time: str = None, arrival_airpot: FlightPointDetails = None, airline: str = None, marketing: FlightAirlineDetails = None, operating: FlightAirlineDetails = None, disclosure_carrier: FlightDisclosureCarrier = None, mariage_group: FlightMarriageGrp = None, seats: str = None, action_code: str = None, segment_special_requests: str = None, schedule_change_indicator: str = None, segment_booked_date: str = None, air_miles_flown: str = None, funnel_flight: str = None, change_of_gauge: str = None, flight_number: str = None, class_of_service: str = None, elapsed_time: str = None, equipment_type: str = None, eticket: str = None, number_in_party: str = None, code: str = None):
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

    def to_data(self):
        return {
            "sequence": self.sequence,
            "res_book_desig_code": self.res_book_desig_code,
            "departure_date_time": self.departure_date_time,
            "departure_airpot": self.departure_airport.to_data() if self.departure_airport is not None else {},
            "arrival_date_time": self.arrival_date_time,
            "arrival_airpot": self.arrival_airpot.to_data() if self.arrival_airpot is not None else {},
            "airline_ref_id": self.airline,
            "marketing": self.marketing.to_data() if self.marketing is not None else {},
            "operating": self.operating.to_data() if self.operating is not None else {},
            "disclosure_carrier": self.disclosure_carrier.to_data() if self.disclosure_carrier is not None else {},
            "mariage_group": self.mariage_group.to_data() if self.mariage_group is not None else {},
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
        self.retrieve_passenger_type()

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
            "last_name": self.last_name,
            "first_name": self.first_name,
            "gender": self.gender,
            "surname": self.sur_name,
            "middle_name": self.middle_name,
            "forename": self.fore_name,
            "action_code": self.action_code,
            "number_in_party": self.number_in_party,
            "vendor_code": self.vendor_code,
            "date_of_birth": self.date_of_birth,
            "passenger_type": self.passenger_type,
            "preferences": self.preferences.to_data()
        }


class FormOfPayment(BasicDataObject):
    """
        Keeps information about form of payments
    """
    def __init__(self, short_text: str = None):
        self.short_text = short_text

    def to_data(self):
        return{
            "short_text": self.short_text
        }


class PriceQuote(BasicDataObject):
    """
        This is to represent a price quote object
    """
    pass


class TicketingInfo(BasicDataObject):
    """
        Represents a ticketing information
    """
    def __init__(self, id: str = None, index: str = None, element_id: str = None, code: str = None, branch_pcc: str = None, date: str = None, time: str = None, queue_number: str = None, comment: str = None):
        self.id = id
        self.index = index
        self.element_id = element_id
        self.code = code
        self.branch_pcc = branch_pcc
        self.date = date
        self.time = time
        self.queue_number = queue_number
        self.comment = comment

    def to_data(self):
        return{
            "id": self.id,
            "index": self.index,
            "element_id": self.element_id,
            "code": self.code,
            "branch_pcc": self.branch_pcc,
            "date": self.date,
            "time": self.time,
            "queue_number": self.queue_number,
            "comment": self.comment,
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
            "itineraries": [i.to_data() for i in self.itineraries],
            "passengers": [p.to_data() for p in self.passengers],
            "formOfPayments": [f.to_data() for f in self.formOfPayments],
            "priceQuotes": [p.to_data() for p in self.priceQuotes],
            "ticketingInfo": self.ticketingInfo.to_data() if self.ticketingInfo is not None else {}
        }


def test_me():
    """
        This function is for testing purpose. It would be removed later.
    """
    r = Reservation()
    p1 = Passenger("Mariama", "KHAN", "F", "2017-03-23", preferences={"hublot": True, "alchol": False})
    p2 = Passenger("Elodie", "DIOUF", "F", "1987-04-04")
    r.addPassenger(p1).addPassenger(p2)
    firstItinerary = Itinerary("OUTBOUND")
    dep = FlightPointDetails("2019-06-27", "13", -4, "NYC", "JFK", "I", "B")
    arr = FlightPointDetails("2019-06-27", "16", +2, "PAR", "CDG", "4", "F")
    firstItinerary.addSegment(FlightSegment(1, dep, arr, "AA", "1998", "B", "01.54"))
    secondItinerary = Itinerary("INBOUND")
    r.addItinerary(firstItinerary).addItinerary(secondItinerary)
    print(r.to_json())


if __name__ == "__main__":
    test_me()
