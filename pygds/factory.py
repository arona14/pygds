from pygds.sabre.sabre_gds import SabreGDS
from pygds.amadeus.amadeus_gds import AmadeusGDS
from pygds.core.abstract_gdsfactory import AbstractGDSFactory
from pygds.core.abstract_gds import AbstractGDS


class GDS(AbstractGDSFactory):

    def __init__(self, gds: str):
        super(GDS, self).__init__(AbstractGDS.of(gds))

    def get_reservation(self, pnr):
        if self.gds_handler is not None:
            return self.gds_handler.get_reservation(pnr)

        else:
            raise NotImplementedError
