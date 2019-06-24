from .core.abstractGDS import AbstractGDS
from .errors.gdserrors import GDSNotFoundError
import logging
class GDSRegistry(object):
    logger = logging.getLogger("GDSRegistry")
    #logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    class __GDSRegistry():
        #logger = GDSRegistry.logger
        """
        This inner class is a proxy to implement Singleton Pattern
        """
        def __init__(self):
            self.all_gds = {}

        def register(self, gds_code: str, gds: AbstractGDS):
            """
                This method registers a GDS in the Repository. So it can be retrieved by the given code
            """
            if gds is None:
                GDSRegistry.logger.error("calling register with a null GDS.")
                raise ValueError("The GDS object cannot be null.")
            self.all_gds[gds_code] = gds
            GDSRegistry.logger.info(f"Registred GDS with code {gds_code}")

        def unregister(self, gds_code):
            """
                Unregistering a GDS is forgettting it form the Repository
            """
            try:
                del self.all_gds[gds_code]
            except KeyError:
                GDSRegistry.logger.warn(f"Trying to unregister non existing GDS from the repository ('{gds_code}')")
            GDSRegistry.logger.info(f"Succesfully unregistred GDS with code '{gds_code}'")

        def getGDSByCode(self, code: str):
            """
                This is for retrieving a GDS by giving it's code. It may raise a GDSNotFoundError if the GDS doesn't exists.
            """
            if code is None:
                raise ValueError("The code of GDS cannot be null")
            gds = self.all_gds.get(code)
            if gds is None:
                raise GDSNotFoundError(code)
            return gds

        def of(self, code: str):
            """
                This is alias of getGDSByCode
            """
            return self.getGDSByCode(code)
    instance = None

    def __init__(self):
        """
            This init method ensures that we only have one single instance of our Proxy Class
        """
        if not GDSRegistry.instance:
            GDSRegistry.instance = GDSRegistry.__GDSRegistry()
    
    def __getattr__(self, name: str):
        """
            This method routes all calls to the Proxy Class
        """
        return getattr(self.instance, name)