
from pygds.objectxml import _Ojectxml
from pygds.pricequote import _Pricequote
from pygds.revalidateitinerary import _Revalidateitinerary
from pygds.sabresoapapi import _Sabresoapapi
from pygds.sendmail import _Semdmail
from pygds.ticketing import _Ticketing
import jxmlease,requests
from time import gmtime, strftime


class Gds(object):

    def __init__(self,test):
        self._test=test
         

    @classmethod
    def test_sabre(cls):
        test='test0'
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
