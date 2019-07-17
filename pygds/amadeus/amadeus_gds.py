from pygds.core import abstract_gds


class AmadeusGDS(abstract_gds.AbstractGDS):

    def __init__(self):
        super().__init__("AMADEUS")

    def get_reservation(self, pnr, pcc: str, conversation_id: str):
        return "Reservation data for " + pnr + " in " + self.gds_name

    def search_flights(self, parameter_list):
        pass

    def create_reservation(self, parameter_list):
        pass

    def price(self, parameter_list):
        pass

    def ticket(self, parameter_list):
        pass

    def void(self, parameter_list):
        pass

    def cancel(self, parameter_list):
        pass

    def exchange_segment(self, parameter_list):
        pass

    def refund(self, parameter_list):
        pass

    def rebook_segment(self, parameter_list):
        pass

    def update_passenger(self, parameter_list):
        pass
