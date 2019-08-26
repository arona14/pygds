import unittest
from pygds.sabre import helpers


class TestHelpers(unittest.TestCase):

    def test_soap_to_json_transform(self):

        res = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                <eb:From>
                    <eb:PartyId />
                </eb:From>
                <eb:To>
                    <eb:PartyId />
                </eb:To>
                <eb:CPAId>WR17</eb:CPAId>
                <eb:ConversationId>cosmo-material-af56e540-6b64-11e9-85c5-632661a24895</eb:ConversationId>
                <eb:Service>OTA_AirPriceLLSRQ</eb:Service>
                <eb:Action>OTA_AirPriceLLSRQ</eb:Action>
                <eb:MessageData>
                    <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                    <eb:Timestamp>2019-04-30T21:38:27Z</eb:Timestamp>
                </eb:MessageData>
                </eb:MessageHeader>
                <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                <eb:BinarySecurityToken>Shared/IDL:IceSess\\/SessMgr:1\\.0.IDL/Common/!ICESMS\\/RESA!ICESMSLB\\/RES.LB!-3022701178061931638!1467472!0</eb:BinarySecurityToken>
                </eb:Security>
            </soapenv:Header>
            <soapenv:Body>
                <OTA_AirPriceRQ Version="2.17.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <PriceRequestInformation Retain="true">
                    <OptionalQualifiers>
                        <MiscQualifiers><Commission Percent='10.0'/>
                            <TourCode><SuppressIT Ind='true'/><Text>815ZU</Text></TourCode>
                        </MiscQualifiers>
                        <PricingQualifiers>
                            <CommandPricing RPH="1">
                                <FareBasis TicketDesignator="PP10"/>
                            </CommandPricing>
                            <ItineraryOptions><SegmentSelect Number='1'/><SegmentSelect Number='2'/></ItineraryOptions>
                            <NameSelect NameNumber='01.01'/>
                            <PassengerType Code='ADT' Quantity='1'/>
                        </PricingQualifiers>
                    </OptionalQualifiers>
                    </PriceRequestInformation>
                </OTA_AirPriceRQ>
            </soapenv:Body>
        </soapenv:Envelope>"""

        self.assertTrue(isinstance(helpers.get_data_from_json(res, "OTA_AirPriceRQ"), dict))


if __name__ == '__main__':
    unittest.main()
