from pygds.core.abstract_gds import AbstractGDS


class AmadeusGDS(AbstractGDS):

    def __init__(self):
        super(AmadeusGDS, self).__init__("AMADEUS")

    def get_reservation(self, pnr):
        print("Reservation data for " + pnr + " in " + self.gds_name)
