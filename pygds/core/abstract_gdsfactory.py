# Methods in this class are not complete yet

"""Abstract Factory GDS classes file"""

from abc import ABC, abstractmethod
from pygds.core.abstract_gds import AbstractGDS


class AbstractGDSFactory(ABC):
    """This class implements an Abstract Factory Design Pattern
    which will help choose dynamically the correct GDS.
    """

    def __init__(self, handler: AbstractGDS = None):
        self.gds_handler = handler
        super().__init__()

    @abstractmethod
    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
        pass
