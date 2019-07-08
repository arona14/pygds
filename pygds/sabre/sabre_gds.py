# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

from pygds.core.abstract_gds import AbstractGDS
from pygds.sabre.reservation import SabreReservation


class SabreGDS(AbstractGDS):

    code = "SB"

    def __init__(self):
        super().__init__("SABRE")

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
        print(f"{self.gds_name} get reservation for {pnr}.")

        return SabreReservation().get(pnr, pcc, conversation_id)


def main():
    pass


if __name__ == '__main__':
    main()
