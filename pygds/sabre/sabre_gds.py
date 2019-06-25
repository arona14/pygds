from pygds.core.abstract_gds import AbstractGDS
from pygds.sabre.reservation import SabreReservation


class SabreGDS(AbstractGDS):

    code = "SB"

    def __init__(self):
        super().__init__("SABRE")

    def get_reservation(self, pnr):
        print("Reservation data for " + pnr + " in " + self.gds_name)

        # TODO: These following lines are not permanents. It only here from a refactoring process
        return SabreReservation().get(pnr, "WR17", "pygds-test")
