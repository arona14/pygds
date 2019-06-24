from .sabre.sabregds import SabreGDS
from .amadeus.amadeusgds import AmadeusGDS
from .core.abstractgdsfactory import AbstractGDSFactory


class GDS(AbstractGDSFactory):

    def __init__(self, gds: str):
        if gds.upper() == 'SABRE':
            super(GDS, self).__init__(SabreGDS())

        elif gds.upper() == 'AMADEUS':
            super(GDS, self).__init__(AmadeusGDS())

        else:
            super(GDS, self).__init__()

    def get_reservation(self, pnr):
        if self.gds_handler is not None:
            self.gds_handler.get_reservation(pnr)

        else:
            raise NotImplementedError
