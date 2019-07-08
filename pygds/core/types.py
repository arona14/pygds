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


class FlightPointDetails(BasicDataObject):
    """
        Information about flight point details (on departure or arrival)
    """
    def __init__(self, date: str = None, time: str = None, gmtOffset: int = None, city: str = None, airport: str = None, gate: str = None, terminal: str = None):
        self.date = date
        self.time = time
        self.gmtOffset = gmtOffset
        self.city = city
        self.airport = airport
        self.gate = gate
        self.terminal = terminal

    def to_data(self):
        return {
            "date": self.date,
            "time": self.time,
            "gmtOffset": self.gmtOffset,
            "city": self.city,
            "airport": self.airport,
            "gate": self.gate,
            "terminal": self.terminal
        }


class FlightSegment(BasicDataObject):
    """
        Holds information about a segment
    """
    def __init__(self, sequence: int = 1, departure: FlightPointDetails = None, arrival: FlightPointDetails = None, airline: str = None, flightNumber: str = None, classOfService: str = None, elapsedTime: str = None):
        self.sequence = sequence
        self.departure = departure
        self.arrival = arrival
        self.airline = airline
        self.flightNumber = flightNumber
        self.classOfService = classOfService
        self.elapsedTime = elapsedTime

    def to_data(self):
        return {
            "sequence": self.sequence,
            "departure": self.departure.to_data() if self.departure is not None else {},
            "arrival": self.arrival.to_data() if self.arrival is not None else {},
            "airline": self.airline,
            "flightNumber": self.flightNumber,
            "classOfService": self.classOfService,
            "elapsedTime": self.elapsedTime
        }


class Itinerary(BasicDataObject):
    """
        Holds information about an itinerary
    """
    def __init__(self, itineraryType: str = None):
        self.segments: List[FlightSegment] = []
        self.itineraryType = itineraryType
        self.elapsedTime = None

    def addSegment(self, segment: FlightSegment):
        """
            Adds a new segment to an itinerary
        """
        self.segments.append(segment)
        return self

    def to_data(self):
        return {
            "segments": [s.to_data() for s in self.segments],
            "itineraryType": self.itineraryType,
            "elapsedTime": self.elapsedTime
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
    def __init__(self, firstName: str = None, lastName: str = None, gender: str = None, dateOfBirth: str = None, passengerType: str = None, preferences=None):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.passengerType = passengerType
        self.preferences = preferences if isinstance(preferences, PassengerPreferences) else PassengerPreferences(preferences) if isinstance(preferences, dict) else PassengerPreferences({})
        self.retrievePassengerType()

    def retrievePassengerType(self):
        """
            This method retrieves the passenger type from the age
        """
        if self.dateOfBirth is not None:
            age = datetime.date.today() - datetime.date.fromisoformat(self.dateOfBirth)
            age = age.days / 365
            if age < 0:
                self.passengerType = None
            elif age <= 2:
                self.passengerType = "INFANT"
            elif age <= 12:
                self.passengerType = "CHILD"
            else:
                self.passengerType = "ADULT"

    def to_data(self):
        return {
            "lastName": self.lastName,
            "firstName": self.firstName,
            "gender": self.gender,
            "dateOfBirth": self.dateOfBirth,
            "passengerType": self.passengerType,
            "preferences": self.preferences.to_data()
        }


class FormOfPayment(BasicDataObject):
    """
        Keeps information about form of payments
    """
    pass


class PriceQuote(BasicDataObject):
    """
        This is to represent a price quote object
    """
    pass


class TicketingInfo(BasicDataObject):
    """
        Represents a ticketing information
    """
    pass


class Reservation(BasicDataObject):
    """
        A class to keep all data about reservation
    """
    def __init__(self):
        self.itineraries: List[Itinerary] = []
        self.passengers: List[Passenger] = []
        self.formOfPayments: List[FormOfPayment] = []
        self.priceQuotes: List[PriceQuote] = []
        self.ticketingInfo: TicketingInfo = None

    def addItinerary(self, itnr: Itinerary):
        """
            Add a new itinerary to the reservation
        """
        self.itineraries.append(itnr)
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


class SellItinerary(BasicDataObject):

    def __init__(self, origin, destination, departure_date, company, flight_number, booking_class, quantity):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.company = company
        self.flight_number = flight_number
        self.booking_class = booking_class
        self.quantity = quantity


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
