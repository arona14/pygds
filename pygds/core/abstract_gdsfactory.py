# Methods in this class are not complete yet

"""Abstract Factory GDS classes file"""

import abc
from pygds.core import abstract_gds


class AbstractGDSFactory(abc.ABC):
    """This class implements an Abstract Factory Design Pattern
    which will help choose dynamically the correct GDS.
    """

    def __init__(self, handler: abstract_gds.AbstractGDS = None):
        self.gds_handler = handler
        super().__init__()

    @abc.abstractmethod
    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
