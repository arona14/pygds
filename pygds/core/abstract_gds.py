# Methods in this class are not complete yet

"""Abstract GDS classes file"""

from abc import ABCMeta, abstractmethod


class AbstractGDS(metaclass=ABCMeta):
    """
    The GDS Meta class that register all derived class.
    It implements a static 'of' method that will help finding a registered class based
    on it's name.
    """

    code = None

    def __init__(self, name: str):
        self.gds_name = name
        super().__init__()

    @abstractmethod
    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
        pass

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
