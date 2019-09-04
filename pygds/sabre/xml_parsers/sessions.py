from pygds.core.helpers import get_data_from_xml as from_xml, get_data_from_json_safe as json_safe
from pygds.core.sessions import SessionInfo
from pygds.sabre.xml_parsers.response_extractor import BaseResponseExtractor


class SessionExtractor(BaseResponseExtractor):

    def __init__(self, xml_content: str):
        super().__init__(xml_content, False, False)

    def extract(self):
        response = super().extract()
        response.session_info = response.payload
        return response

    def _extract(self):
        header = from_xml(self.xml_content, "soap-env:Envelope", "soap-env:Header")
        token = json_safe(header, "wsse:Security", "wsse:BinarySecurityToken", "#text")
        header = json_safe(header, "eb:MessageHeader")
        conversation_id = json_safe(header, "eb:ConversationId")
        session_id = json_safe(header, "eb:MessageData", "eb:MessageId")

        return SessionInfo(token, 1, session_id, conversation_id, False)
