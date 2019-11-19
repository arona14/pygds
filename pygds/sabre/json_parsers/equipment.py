import json
import logging
from pygds.core.sessions import SessionInfo
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe


class AircraftInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class AircraftInfo(AircraftInfoBasic):

    def __init__(self):
        self.air_craft_info: list = []  # the travel itinerary

    def to_dict(self):
        return {
            "AircraftInfo": self.air_craft_info
        }


class BaseResponseRestExtractor(object):
    """
        This is a base class for all response extractor. A helpful class to extract useful info from an Json.
    """

    def __init__(self, json_content: str, parse_session: bool = True, parse_app_error: bool = True):
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
            self.app_error = AircraftErrorExtractor(self.json_content).extract().application_error
        return GdsResponse(None, self.default_value() if self.app_error else self._extract(), self.app_error)

    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class AircraftErrorExtractor(BaseResponseRestExtractor):
    """
    Extract application error from response
    """

    def __init__(self, json_content: str):
        super().__init__(json_content, False, False)

    def extract(self):
        response = super().extract()
        response.application_error = response.payload
        return response

    def _extract(self):
        self.json_content = json.loads((self.json_content).decode('utf8').replace("'", '"'))
        payload = from_json(self.json_content)
        app_error_data = from_json_safe(payload, "ApplicationResults", "Error")
        if not app_error_data:
            return None
        return ApplicationError(None, None, None, app_error_data)


class AircraftExtractor(BaseResponseRestExtractor):

    def __init__(self, json_content):
        super().__init__(json_content)

    def _extract(self):

        aircraft = AircraftInfo()
        aircraft.air_craft_info = json.loads(self.json_content)["AircraftInfo"]
        return aircraft.air_craft_info
