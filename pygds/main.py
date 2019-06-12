from .sabre.reservation import SabreReservation
from .sabre.command import SabreCommand
from .sabre.session import SabreSession

class GDS:

    def get_reservation(self, gds, pnr, pcc, conversation_id=None):

        if gds.upper() == 'SABRE':
            return SabreReservation().get(pnr, pcc, conversation_id)
        else:
            return 'Not yet implemented'

    def send_command(self, gds, command, pcc, token = None, pnr = None, conversation_id = None ) :

        if gds.upper() == 'SABRE' :

            if token == None :
                token = SabreSession().open(pcc,conversation_id)
            #if pnr == None :
            #    pnr = SabreReservation().get(pnr, pcc, conversation_id)
            commandresponse = SabreCommand().send(command, pcc, token, conversation_id)

            SabreSession().close(pcc,token,conversation_id)
            #print(closesessionresponse)
            return commandresponse

