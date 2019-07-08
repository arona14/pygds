from pygds.core import abstract_gds


class AmadeusGDS(abstract_gds.AbstractGDS):

    code = "AM"

    def __init__(self):
        super().__init__("AMADEUS")

    def get_reservation(self, pnr):
        print("Reservation data for " + pnr + " in " + self.gds_name)
        return "Reservation data for " + pnr + " in " + self.gds_name
