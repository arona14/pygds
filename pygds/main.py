from .sabre.reservation import SabreReservation
from .sabre.command import SabreCommand
from .sabre.session import SabreSession
from .sabre.transaction import SabreTransaction

class GDS:

    def get_reservation(self, gds, pnr, pcc, conversation_id=None):

        if gds.upper() == 'SABRE':
            return SabreReservation().get(pnr, pcc, conversation_id)
        else:
            return 'Not yet implemented'

    def send_command(self, gds, command, pcc, token = None, pnr = None, conversation_id = None) :

        if gds.upper() == 'SABRE' :

            commandresponse = SabreCommand().send(command, pcc, token, conversation_id)

            
            return commandresponse

    def end_transaction(self, gds, pcc, token, conversation_id) :

        """Call end Transacton method"""
        if gds.upper() == 'SABRE' :

            end_transaction_response = SabreTransaction().end(pcc,token,conversation_id)

            return end_transaction_response
        else :
            return 'Not yet implemented'



