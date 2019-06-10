from pygds.sabre.reservation import SabreReservation

class GDS ():

    def get_reservation(self,gds=None, pnr=None, pcc=None, conversation_id=None):

        if gds.upper() == 'SABRE':
            return SabreReservation().get(pnr, pcc, conversation_id)
        else:
            return 'Not yet implemented'
