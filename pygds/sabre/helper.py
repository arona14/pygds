import json
import xmltodict


def fromSoapResponse(response):
    """Return Json dic"""
    try:
        get_reservation = json.loads(json.dumps(xmltodict.parse(response.content)))
        if get_reservation is not None:
            toreturn_reservation = get_reservation["soap-env:Envelope"]["soap-env:Body"]#["stl19:GetReservationRS"]
            toreturn_reservation = str(toreturn_reservation).replace("@", "")
            toreturn_dict = eval(toreturn_reservation.replace("u'", "'"))
            del toreturn_dict["xmlns:stl19"]
            del toreturn_dict["xmlns:ns6"]
            del toreturn_dict["xmlns:or114"]
            del toreturn_dict["xmlns:raw"]
            del toreturn_dict["xmlns:ns4"]
        return toreturn_dict
    except:
        toreturn_dict = None
    return toreturn_dict