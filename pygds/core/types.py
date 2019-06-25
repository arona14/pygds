from typing import List
class Itinerary(object):
    pass
class Passenger(object):
    pass

class FormOfPayment(object):
    pass

class PriceQuote(object):
    pass

class TicketingInfo(object):
    pass

class Reservation(object):
    def __init__(self):
        self.itineraries : List[Itinerary] = []
        self.passengers : List[Passenger] = []
        self.formOfPayments : List[FormOfPayment] = []
        self.priceQuotes : List [PriceQuote] = []
        self.ticketingInfo : TicketingInfo = None

    def addItinerary(self, itnr : Itinerary):
        self.itineraries.append(itnr)

    def addPassengers(self, psgr: List[Passenger]):
        self.passengers = psgr

    def addFormOfPayments(self, fps = List[FormOfPayment]):
        self.formOfPayments = fps

    def toJson(self):
        return f"""
        """