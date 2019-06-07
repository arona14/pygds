
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

    def getreservation(self,data=None):

        """

		"""
        
        def get_booking_detail():

            bd_data = {}
            bd_data['RecordLocator'] = data["stl18:Reservation"]\
            ["stl18:BookingDetails"]["stl18:RecordLocator"]
            bd_data['CreationTimestamp'] = data["stl18:Reservation"]\
            ["stl18:BookingDetails"]["stl18:CreationTimestamp"]
            bd_data['SystemCreationTimestamp'] = data["stl18:Reservation"]\
            ["stl18:BookingDetails"]["stl18:SystemCreationTimestamp"]
            bd_data['CreationAgentID'] = data["stl18:Reservation"]\
            ["stl18:BookingDetails"]["stl18:CreationAgentID"]
            bd_data['UpdateTimestamp'] = data["stl18:Reservation"]\
            ["stl18:BookingDetails"]["stl18:UpdateTimestamp"]
            bd_data['BookingSource'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["BookingSource"]
            bd_data['AgentSine'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["AgentSine"]
            bd_data['PseudoCityCode'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["PseudoCityCode"]
            bd_data['ISOCountry'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["ISOCountry"]
            bd_data['AgentDutyCode'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["AgentDutyCode"]
            bd_data['AirlineVendorID'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["AirlineVendorID"]
            bd_data['HomePseudoCityCode'] = data["stl18:Reservation"]["stl18:POS"]\
            ["stl18:Source"]["HomePseudoCityCode"]
            return bd_data

        def get_passengers():

            passenger_data = data["stl18:Reservation"]["stl18:PassengerReservation"]\
            ["stl18:Passengers"]["stl18:Passenger"]
            pass_list = []
            if type(passenger_data) == list:
                for passenger in passenger_data:
                    p = {}
                    pass_request = passenger['stl18:SpecialRequests']['stl18:APISRequest']
                    p['passengerType'] = passenger['passengerType']
                    p['LastName'] = passenger['stl18:LastName']
                    p['FirstName'] = passenger['stl18:FirstName']
                    if type(pass_request) == list:
                        p['DateOfBirth'] = pass_request[0]['stl18:DOCSEntry']['stl18:DateOfBirth']
                        p['Gender'] = pass_request[0]['stl18:DOCSEntry']['stl18:Gender']
                        p['Surname'] = pass_request[0]['stl18:DOCSEntry']['stl18:Surname']
                        p['Forename'] = pass_request[0]['stl18:DOCSEntry']['stl18:Forename']
                        p['MiddleName'] = pass_request[0]['stl18:DOCSEntry']['stl18:MiddleName']
                    else:
                        p['DateOfBirth'] = pass_request['stl18:DOCSEntry']['stl18:DateOfBirth']
                        p['Gender'] = pass_request['stl18:DOCSEntry']['stl18:Gender']
                        p['Surname'] = pass_request['stl18:DOCSEntry']['stl18:Surname']
                        p['Forename'] = pass_request['stl18:DOCSEntry']['stl18:Forename']
                        p['MiddleName'] = pass_request['stl18:DOCSEntry']['stl18:MiddleName']
                    pass_list.append(p)
            else:
                p = {}
                pass_request = passenger_data['stl18:SpecialRequests']['stl18:APISRequest']
                p['passengerType'] = passenger_data['passengerType']
                p['LastName'] = passenger_data['stl18:LastName']
                p['FirstName'] = passenger_data['stl18:FirstName']
                if type(pass_request) == list:
                    p['DateOfBirth'] = pass_request[0]['stl18:DOCSEntry']['stl18:DateOfBirth']
                    p['Gender'] = pass_request[0]['stl18:DOCSEntry']['stl18:Gender']
                    p['Surname'] = pass_request[0]['stl18:DOCSEntry']['stl18:Surname']
                    p['Forename'] = pass_request[0]['stl18:DOCSEntry']['stl18:Forename']
                    p['MiddleName'] = pass_request[0]['stl18:DOCSEntry']['stl18:MiddleName']
                else:
                    p['DateOfBirth'] = pass_request['stl18:DOCSEntry']['stl18:DateOfBirth']
                    p['Gender'] = pass_request['stl18:DOCSEntry']['stl18:Gender']
                    p['Surname'] = pass_request['stl18:DOCSEntry']['stl18:Surname']
                    p['Forename'] = pass_request['stl18:DOCSEntry']['stl18:Forename']
                    p['MiddleName'] = pass_request['stl18:DOCSEntry']['stl18:MiddleName']
                pass_list.append(p)
            return pass_list