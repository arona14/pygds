import json
import logging

from pygds.core.sessions import SessionInfo
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.app_error import ApplicationError
from pygds.core.helpers import get_data_from_json as from_json, get_data_from_json_safe as from_json_safe


class BaseResponseRevalidateExtractor(object):
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
            self.app_error = AppErrorRevalidateExtractor(self.json_content, self.main_tag).extract().application_error
        return GdsResponse(None, self.default_value() if self.app_error else self._extract(), self.app_error)

    def _extract(self):
        """
            A private method that does the work of extracting useful data.
        """
        raise NotImplementedError("Sub class must implement '_extract' method")


class AppErrorRevalidateExtractor(BaseResponseRevalidateExtractor):
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
        payload = from_json(self.json_content)
        app_error_data = from_json_safe(payload, "errorCode")
        if not app_error_data:
            return None

        message_error = from_json_safe(payload, "message")
        return ApplicationError(None, None, None, message_error)


class RevalidateItinerarieInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class RevalidateItinerarieInfo(RevalidateItinerarieInfoBasic):

    def __init__(self):
        self.status: str = None  # status response
        self.brand_feature: dict = None  # brand_feature response
        self.priced_itinerarie: dict = None  # priced_itinerarie response
        self.tpa_extension: dict = None  # tpa_extension response

    def to_dict(self):
        return {
            "Status": self.status,
            "BrandFeatures": self.brand_feature,
            "PricedItineraries": self.priced_itinerarie,
            "TPA_Extensions": self.tpa_extension
        }


class RevalidateItineraryExtractor(BaseResponseRevalidateExtractor):
    """
    This class retrieves information for revalidate itinerary
    """
    def __init__(self, json_content):
        super().__init__(json_content, main_tag="OTA_AirLowFareSearchRS")

    def _extract(self):
        revalidate_itinerarie = RevalidateItinerarieInfo()
        self.json_content = json.loads((self.json_content).decode('utf8').replace("'", '"'))
        payload = from_json_safe(self.json_content, "OTA_AirLowFareSearchRS")

        revalidate_itinerarie.status = from_json_safe(payload, "Success")
        revalidate_itinerarie.brand_feature = from_json_safe(payload, "BrandFeatures")
        revalidate_itinerarie.priced_itinerarie = from_json_safe(payload, "PricedItineraries")
        revalidate_itinerarie.tpa_extension = from_json_safe(payload, "TPA_Extensions")

        return revalidate_itinerarie
