import fnc
from pygds.amadeus.xml_parsers.response_extractor import BaseResponseExtractor
from pygds.core.types import PassengerBasicInfo
from pygds.core.price import TSTInfo
from pygds.core.helpers import get_data_from_xml as from_xml, ensure_list


class CreateTstResponseExtractor(BaseResponseExtractor):
    """
    Wil extract response of create TST from price
    """

    def __init__(self, xml_content):
        super().__init__(xml_content, True, True, "Ticket_CreateTSTFromPricingReply")

    def _extract(self):
        payload = from_xml(self.xml_content, "soapenv:Envelope", "soapenv:Body", "Ticket_CreateTSTFromPricingReply")
        pnr = None
        status = None
        for reservation in ensure_list(fnc.get("pnrLocatorData.reservation", payload)):
            if not pnr:
                pnr = fnc.get("controlNumber", reservation)
            if fnc.get("controlType") == "5":
                status = fnc.get("controlNumber", reservation)
            if pnr and status:
                break
        all_tst = []
        for tst_data in ensure_list(fnc.get("tstList", payload, default=[])):
            tst_ref = fnc.get("tstReference.uniqueReference", tst_data)
            all_passengers = []
            for p in ensure_list(fnc.get("paxInformation.refDetails", tst_data, default=[])):
                passenger_type = fnc.get("refQualifier", p)
                passenger_ref = fnc.get("refNumber", p)
                all_passengers.append(PassengerBasicInfo(passenger_ref, passenger_type))
            tst_info = TSTInfo(status=status, pnr=pnr, tst_ref=tst_ref, passengers=all_passengers)
            all_tst.append(tst_info)
        return all_tst
