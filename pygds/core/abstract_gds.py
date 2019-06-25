# Methods in this class are not complete yet


from abc import ABCMeta, abstractmethod


class AbstractGDS(metaclass=ABCMeta):

    def __init__(self, name):
        self.gds_name = name
        super(AbstractGDS, self).__init__()

    @abstractmethod
    def get_reservation(self, pnr):
        pass

    @staticmethod
    def of(key: str):
        gds = [cls for cls in AbstractGDS.__subclasses__() if key.upper() in cls.__name__.upper()]

        if len(gds):
            return gds[0]
        else:
            return None
