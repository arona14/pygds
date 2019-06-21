from .sabre.reservation import SabreReservation
from .sabre.command import SabreCommand
from .sabre.transaction import SabreTransaction


class GDS:

    def __init__(self, gds):
        if gds.upper() == 'SABRE':
            self.reservation_handler = SabreReservation()
            self.command_handler = SabreCommand()
            self.transaction_handler = SabreTransaction()
        else:
            self.reservation_handler = None
            self.command_handler = None
            self.transaction_handler = None

    def get_reservation(self, pnr, pcc, conversation_id=None):

        self.reservation_handler.get(pnr, pcc, conversation_id)

    def send_command(self, command, pcc, token=None, pnr=None, conversation_id=None):

        command_response = self.command_handler.send(command, pcc, token, conversation_id)

        return command_response

    def end_transaction(self, pcc, token, conversation_id):
        """End a transaction which will try to save the current changes in the instance"""

        end_transaction_response = self.transaction_handler.end(pcc, token, conversation_id)

        return end_transaction_response
