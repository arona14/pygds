import json
import logging

import fnc
from pygds.core.sessions import SessionInfo
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe
from pygds.sabre.json_parsers.create_passenger_name_record import CreatePnrInfo
from pygds.sabre.json_parsers.equipment import AircraftInfo


class BaseResponseRestExtractor(object):
    """
        This is a base class for all response extractor. A helpful class to extract useful info from an Json.
    """

    def __init__(self, json_content: str, parse_session: bool = True, parse_app_error: bool = True,
                 main_tag: str = None):
        """
        constructor for base class
        :param json_content: The content as JSON
        :param parse_session: A boolean to tell if we will the session part
        :param parse_app_error: A boolean to tell if we will parse application error part
        :param main_tag: The main tag of the reply
        """
        self.json_content = json_content
        self.parse_session = parse_session
        self.parse_app_error = parse_app_error
        self.main_tag = main_tag
        self.log = logging.getLogger(str(self.__class__))
        self.session_info: SessionInfo = None
        self.app_error: ApplicationError = None

    def default_value(self):
        return None

    def extract(self):
        """
        The public method to call when extracting useful data.
        :return: GdsResponse
        """
        if self.parse_app_error and self.app_error is None:
            self.app_error = AppErrorRestExtractor(self.json_content, self.main_tag).extract().application_error
        return GdsResponse(None, self.default_value() if self.app_error else self._extract(), self.app_error)

    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class AppErrorRestExtractor(BaseResponseRestExtractor):
    """
    Extract application error from response
    """

    def __init__(self, json_content: str, main_tag: str):
        super().__init__(json_content, False, False, main_tag)

    def extract(self):
        response = super().extract()
        response.application_error = response.payload
        return response

    def _extract(self):
        self.json_content = json.loads((self.json_content).decode('utf8').replace("'", '"'))
        if self.main_tag is not None:
            payload = from_json(self.json_content, self.main_tag)
        else:
            payload = from_json(self.json_content)
        app_error_data = from_json_safe(payload, "ApplicationResults", "Error")
        if not app_error_data:
            return None

        return ApplicationError(None, None, None, app_error_data)


class CreatePnrExtractor(BaseResponseRestExtractor):

    def __init__(self, json_content):
        super().__init__(json_content, main_tag="CreatePassengerNameRecordRS")

    def _extract(self):

        create_pnr_info = CreatePnrInfo()
        self.json_content = json.loads((self.json_content).decode('utf8').replace("'", '"'))
        payload = from_json(self.json_content, "CreatePassengerNameRecordRS")

        status = fnc.get('ApplicationResults.status', payload, default="")
        air_book = fnc.get('AirBook', payload, default={})
        air_price = fnc.get('AirPrice', payload, default={})
        travel_itinerary_read = fnc.get('TravelItineraryRead', payload, default={})
        itinerary_ref = fnc.get('ItineraryRef.ID', payload, default={})

        create_pnr_info.status = status
        create_pnr_info.itinerary_ref = itinerary_ref
        create_pnr_info.air_book = air_book
        create_pnr_info.air_price = air_price
        create_pnr_info.travel_itinerary_read = travel_itinerary_read

        return create_pnr_info


class AircraftExtractor(BaseResponseRestExtractor):

    def __init__(self, json_content):
        super().__init__(json_content, main_tag=None)

    def _extract(self):

        aircraft = AircraftInfo()
        aircraft.air_craft_info = json.loads(self.json_content)["AircraftInfo"]
        return aircraft.air_craft_info
