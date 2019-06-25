from pygds.core.abstract_gds import AbstractGDS
from pygds.core.abstract_gdsfactory import AbstractGDSFactory


class GDS(AbstractGDSFactory):

    def __init__(self, gds: str):
        super(GDS, self).__init__(AbstractGDS.of(gds)())

    def get_reservation(self, pnr):
        if self.gds_handler is not None:
            return self.gds_handler.get_reservation(pnr)

        else:
            return None
