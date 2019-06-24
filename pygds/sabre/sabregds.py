from pygds.core.abstractgds import AbstractGDS
from .reservation import SabreReservation


class SabreGDS(AbstractGDS):

    def __init__(self):
        super(SabreGDS, self).__init__("SABRE")

    def get_reservation(self, pnr):
        print("Reservation data for " + pnr + " in " + self.gds_name)

        # TODO: These following lines are not permanents. It only here from a refactoring process
        return SabreReservation().get(pnr, "WR17", "pygds-test")
