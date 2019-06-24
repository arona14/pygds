# Methods in this class are not complete yet


from abc import ABC, abstractmethod


class AbstractGDS(ABC):

    def __init__(self, name):
        self.gds_name = name
        super(AbstractGDS, self).__init__()

    @abstractmethod
    def get_reservation(self, pnr):
        pass
