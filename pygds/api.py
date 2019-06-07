
from pygds.objectxml import _Ojectxml
from pygds.pricequote import _Pricequote
from pygds.revalidateitinerary import _Revalidateitinerary
from pygds.sabresoapapi import _Sabresoapapi
from pygds.sendmail import _Semdmail
from pygds.ticketing import _Ticketing



class Gds(object):

    def __init__(self,test):
        self._test=test
         

    @classmethod
    def sabre(cls):
        test='connecting to SABRE'
        return cls(test)
   


    @property
    def objectxml(self):

        return _Ojectxml(self)

    @property
    def pricequote(self):

        return _Pricequote(self)

    @property
    def revalidateitinerary(self):

        return _Revalidateitinerary(self)

    @property
    def sabresoapapi(self):

        return _Sabresoapapi(self)

    @property
    def sendmail(self):

        return _Semdmail(self)

    @property
    def ticketing(self):
        
        return _Ticketing(self)
