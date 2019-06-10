from pygds.sabre.reservation import SabreReservation

def get_reservation(gds, pnr, pcc, conversation_id):

    if gds.upper() == 'SABRE':
        return SabreReservation().get(pnr, pcc, conversation_id)
    else:
        return 'Not yet implemented'
