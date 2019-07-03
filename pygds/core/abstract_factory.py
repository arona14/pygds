"""Abstract Factory classes file"""

import abc


class AbstractFactory(abc.ABC):
    """This class implements an Abstract Factory Design Pattern
    which will help choose dynamically the correct Class.
    """

    def __init__(self, handler=None):
        self.obj_handler = handler
        super().__init__()

    def __getattr__(self, name: str):
        """
            This method routes all calls to the handler
        """
        return getattr(self.obj_handler, name)


def main():
    pass


if __name__ == '__main__':
    main()
