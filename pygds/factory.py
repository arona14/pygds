from pygds.core import abstract_gds as abs_gds
from pygds.core import abstract_factory as abs_factory


class GDS(abs_factory.AbstractFactory):

    def __init__(self, gds: str):
        super().__init__(abs_gds.AbstractGDS.of(gds)())


def main():
    pass


if __name__ == '__main__':
    main()
