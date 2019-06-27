from pygds.core import abstract_gds as abs_gds
from pygds.core import abstract_gdsfactory as abs_factory


class GDS(abs_factory.AbstractGDSFactory):

    def __init__(self, gds: str):
        super().__init__(abs_gds.AbstractGDS.of(gds)())

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str):
        if self.gds_handler is not None:
            return self.gds_handler.get_reservation(pnr, pcc, conversation_id)

        else:
            return None


def main():
    pass


if __name__ == '__main__':
    main()
