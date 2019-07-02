from typing import List
import json
import datetime


class BasicDataObject(object):
    """
        A basic class that contains data.
    """
    def toData(self):
        """
            Method that returns a dictionary containing useful data. Must be implemented by sub-classes
        """
        raise NotImplementedError(" this is not yet implemented")

    def toJson(self):

        return json.dumps(self.toData(), indent=4)


class FlightPointDetails(BasicDataObject):
    def __init__(self, date: str = None, time: str = None, gmtOffset: int = None, city: str = None, airport: str = None, gate: str = None, terminal: str = None):
        self.date = date
        self.time = time
        self.gmtOffset = gmtOffset
        self.city = city
        self.airport = airport
        self.gate = gate
        self.terminal = terminal

    def toData(self):
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
    def __init__(self, sequence: int = 1, departure: FlightPointDetails = None, arrival: FlightPointDetails = None, airline: str = None, flightNumber: str = None, classOfService: str = None, elapsedTime: str = None):
        self.sequence = sequence
        self.departure = departure
        self.arrival = arrival
        self.airline = airline
        self.flightNumber = flightNumber
        self.classOfService = classOfService
        self.elapsedTime = elapsedTime

    def toData(self):
        return {
            "sequence": self.sequence,
            "departure": self.departure.toData() if self.departure is not None else {},
            "arrival": self.arrival.toData() if self.arrival is not None else {},
            "airline": self.airline,
            "flightNumber": self.flightNumber,
            "classOfService": self.classOfService,
            "elapsedTime": self.elapsedTime
        }


class Itinerary(BasicDataObject):
    def __init__(self, itineraryType: str = None):
        self.segments: List[FlightSegment] = []
        self.itineraryType = itineraryType
        self.elapsedTime = None

    def addSegment(self, segment: FlightSegment):
        self.segments.append(segment)
        return self

    def toData(self):
        return {
            "segments": [s.toData() for s in self.segments],
            "itineraryType": self.itineraryType,
            "elapsedTime": self.elapsedTime
        }


class PassengerPreferences(BasicDataObject):
    def __init__(self, prefs: dict = {}):
        self.prefs = prefs

    def toData(self):
        return self.prefs


class Passenger(BasicDataObject):
    def __init__(self, firstName: str = None, lastName: str = None, gender: str = None, dateOfBirth: str = None, passengerType: str = None, preferences=None):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.passengerType = passengerType
        self.preferences = preferences if isinstance(preferences, PassengerPreferences) else PassengerPreferences(preferences) if isinstance(preferences, dict) else PassengerPreferences({})
        self.retrievePassengerType()

    def retrievePassengerType(self):
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

    def toData(self):
        return {
            "lastName": self.lastName,
            "firstName": self.firstName,
            "gender": self.gender,
            "dateOfBirth": self.dateOfBirth,
            "passengerType": self.passengerType,
            "preferences": self.preferences.toData()
        }


class FormOfPayment(BasicDataObject):
    pass


class PriceQuote(BasicDataObject):
    pass


class TicketingInfo(BasicDataObject):
    pass


class Reservation(BasicDataObject):
    def __init__(self):
        self.itineraries: List[Itinerary] = []
        self.passengers: List[Passenger] = []
        self.formOfPayments: List[FormOfPayment] = []
        self.priceQuotes: List[PriceQuote] = []
        self.ticketingInfo: TicketingInfo = None

    def addItinerary(self, itnr: Itinerary):
        self.itineraries.append(itnr)
        return self

    def addPassenger(self, psgr: Passenger):
        self.passengers.append(psgr)
        return self

    def addFormOfPayment(self, fp: FormOfPayment):
        self.formOfPayments.append(fp)
        return self

    def toData(self):
        return {
            "itineraries": [i.toData() for i in self.itineraries],
            "passengers": [p.toData() for p in self.passengers],
            "formOfPayments": [f.toData() for f in self.formOfPayments],
            "priceQuotes": [p.toData() for p in self.priceQuotes],
            "ticketingInfo": self.ticketingInfo.toData() if self.ticketingInfo is not None else {}
        }


def test_me():
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
    print(r.toJson())


if __name__ == "__main__":
    test_me()
