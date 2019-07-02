# Methods in this class are not complete yet

"""Abstract GDS classes file"""

import abc


class AbstractGDS(metaclass=abc.ABCMeta):
    """
    The GDS Meta class that register all derived class.
    It implements a static 'of' method that will help finding a registered class based
    on it's name.
    """

    code = None

    def __init__(self, name: str):
        self.gds_name = name
        super().__init__()

    def search_flights(self, parameter_list):
        raise NotImplementedError("This method is not yet implemented in the specific GDS")

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
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


    @staticmethod
    def of(key: str):
        """
        This static method will get the correct registered class by it name
        :param key: A substring of the name of a registered class
        :return: If found, returns a class, None if not
        """

        gds = [cls for cls in AbstractGDS.__subclasses__() if key.upper() in cls.__name__.upper()]

        if len(gds):
            return gds[0]
        else:
            return None


def main():
    pass


if __name__ == '__main__':
    main()
