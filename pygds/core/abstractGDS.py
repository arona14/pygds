# Methods in this class are not complete yet


from abc import ABC, abstractmethod


class AbstractGDS(ABC):

    def __init__(self, code, name=None):
        self.gds_code = code
        self.gds_name = code
        super(AbstractGDS, self).__init__()

    def search_flights(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def get_reservation(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def create_reservation(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def price(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def ticket(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def void(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def cancel(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def exchange_segment(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def refund(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def rebook_segment(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def update_passenger(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")


