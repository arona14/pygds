import json
import xmltodict


class FormatSoapAmadeus():

    def soap_service_to_json(self, xml_object):
        """Transform a amadeus soap api response to json format"""
        try:
            json_data = xmltodict.parse(xml_object)
        except:
            json_data = None
        return json_data

    def get_segments(self, dispaly_pnr):
        """ Transform a amadeus json and reponse to json segment list"""
        segments_list = []
        try:
            for data in origin_destination["soapenv:Envelope"]["soapenv:Body"]["PNR_Reply"]["originDestinationDetails"]["itineraryInfo"]:
                segment_data = {}
                dep_date = data["travelProduct"]["product"]["depDate"]
                dep_time = data["travelProduct"]["product"]["depTime"]

                arr_date = data["travelProduct"]["product"]["arrDate"]
                arr_time = data["travelProduct"]["product"]["arrTime"]

                segment_data["departure_airport"] = data["travelProduct"]["boardpointDetail"]["cityCode"]
                segment_data["arrival_airport"] = data["travelProduct"]["offpointDetail"]["cityCode"]
                segment_data["departure_dateTime"] = f"""{dep_date[0:2]}-{dep_date[2:4]}-20{dep_date[4:6]}T{dep_time[0:2]}:{dep_time[2:4]}:00"""
                segment_data["arrival_date_time"] = f"""{arr_date[0:2]}-{arr_date[2:4]}-20{arr_date[4:6]}T{arr_time[0:2]}:{arr_time[2:4]}:00"""
                segment_data['equipment_type'] = data["flightDetail"]["productDetails"]["equipment"]
                segment_data['class_of_service'] = data["travelProduct"]["productDetails"]["classOfService"]

                segments_list.append(segment_data)

        except:
            segments_list = None
        return segments_list

    def get_passengers(self, dispaly_pnr):
          """ Transform a amadeus json and reponse to json passergers list"""
        passengers_list = []
        try:
            for data in traveller_info["soapenv:Envelope"]["soapenv:Body"]["PNR_Reply"]["travellerInfo"]["passengerData"]:
                passenger_data = {}

                surname = data["travellerInformation"]["traveller"]["surname"]
                quantity = data["travellerInformation"]["traveller"]["quantity"]

                firstname = data["travellerInformation"]["traveller"]["firstName"]
                passenger_type = data["travellerInformation"]["traveller"]["type"]

                date = data["dateOfBirth"]["dateAndTimeDetails"]["date"]
                qualifier = data["dateOfBirth"]["dateAndTimeDetails"]["qualifier"]
                date_of_birth = f"""{date[0:2]-[date[2:4]]-{date[4:8]}}"""

                passenger_data['surname'] = surname
                passenger_data['quantity'] = quantity
                passenger_data['firstname'] = firstname
                passenger_data['type']  = passenger_type
                passenger_data['qualifier'] = qualifier
                passenger_data['date_of_birth'] = date_of_birth

                passengers_list.append(passenger_data)
        except:
            passengers_list = None
        return passengers_list


    def get_pnr_infos(self, dispaly_pnr):
         """ Transform a amadeus json and reponse to json pnr infos list"""
        pnr_infos = []
        try:
            for data in pnr_header["soapenv:Envelope"]["soapenv:Body"]["PNR_Reply"]["pnrHeader"]["reservationInfo"]:
                reservation_info = {}
                company_id = data["reservation"]["companyId"]

                control_number = data["reservation"]["controlNumber"]
                date = data["reservation"]["date"]
                time = data["reservation"]["time"]
                date_time = f""" {date[0:2]-{date[2:4]}-20{date[4:6]}T{time[0:2]}:{time[2:4]}}"""
                reservation_info['compagny_id'] = company_id

                reservation_info['control_number'] = control_number
                reservation_info['date_time'] = date_time

                pnr_infos.append(reservation_info)
        except:
            pnr_infos = None
        return pnr_infos


    def get_form_of_payments(self, dispaly_pnr):
        pass

    def get_price_quotes(self, display_pnr):
        pass

    def get_ticketing_info(self, display_pnr):
        pass

    def get_reservation_response(self, xml_object):
        """ Builds the object getResevation """
        reservation_response = {}
        try:
            json_data = self.soap_service_to_json(xml_object)
            itineraries = self.get_segments(json_data)
            passengers = self.get_passengers(json_data)
            form_of_payments = self.get_form_of_payments(json_data)
            price_quotes = self.get_price_quotes(json_data)
            ticketing_info = self.get_price_quotes(json_data)

            reservation_response['itineraries'] = itineraries
            reservation_response['passengers'] = passengers
            reservation_response['form_of_payments'] = form_of_payments
            reservation_response['price_quotes'] = price_quotes
            reservation_response['ticketing_info'] = ticketing_info
        except:
            reservation_response = None
        return reservation_response