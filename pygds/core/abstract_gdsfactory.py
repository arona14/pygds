# Methods in this class are not complete yet


from abc import ABC, abstractmethod
from pygds.core.abstract_gds import AbstractGDS


class AbstractGDSFactory(ABC):

    def __init__(self, handler: AbstractGDS = None):
        self.gds_handler = handler()
        super(AbstractGDSFactory, self).__init__()

    @abstractmethod
    def get_reservation(self, pnr: str):
        pass

