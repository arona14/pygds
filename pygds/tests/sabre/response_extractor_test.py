#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor


xml = """
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
   <soap-env:Header>
      <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" eb:version="1.0" soap-env:mustUnderstand="1">
         <eb:From>
            <eb:PartyId eb:type="URI" />
         </eb:From>
         <eb:To>
            <eb:PartyId eb:type="URI" />
         </eb:To>
         <eb:CPAId>WR17</eb:CPAId>
         <eb:ConversationId>a72340f5-a581-4e24-84ab-ee5eb8f338e4</eb:ConversationId>
         <eb:Service>Session</eb:Service>
         <eb:Action>OTA_AirPriceLLSRS</eb:Action>
         <eb:MessageData>
            <eb:MessageId>7002648707490670230</eb:MessageId>
            <eb:Timestamp>2019-08-23T19:39:10</eb:Timestamp>
            <eb:RefToMessageId>mid:20001209-133003-2333@clientofsabre.com</eb:RefToMessageId>
         </eb:MessageData>
      </eb:MessageHeader>
      <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext">
         <wsse:BinarySecurityToken valueType="String" EncodingType="wsse:Base64Binary">Shared/IDL:IceSess\\/SessMgr:1\\.0.IDL/Common/!ICESMS\\/RESC!ICESMSLB\\/RES.LB!-2981976804729831552!1105674!0</wsse:BinarySecurityToken>
      </wsse:Security>
   </soap-env:Header>
   <soap-env:Body>
      <OTA_AirPriceRS xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:stl="http://services.sabre.com/STL/v01" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2.17.0">
         <stl:ApplicationResults status="Complete">
            <stl:Success timeStamp="2019-08-23T14:39:10-05:00" />
         </stl:ApplicationResults>
         <PriceQuote>
            <MiscInformation>
               <BaggageInfo>
                  <SubCodeProperties RPH="1" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>PT</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="PH">
                        <Text>IN HOLD</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>PET IN HOLD</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0BSAEDL</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="2" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>PT</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="PC">
                        <Text>IN CABIN</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>PET IN CABIN</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0BTAEDL</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="3" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <CommercialNameofBaggageItemType>FREE BAGGAGE ALLOWANCE</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0DFAADL</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="4" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <CommercialNameofBaggageItemType>UPTO 22LB 10KG AND45LI 115LCM</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="10">
                        <Text>UP TO 22 POUNDS/10 KILOGRAMS</Text>
                     </DescriptionOne>
                     <DescriptionTwo Code="4U">
                        <Text>UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                     </DescriptionTwo>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0E3ACDL</ExtendedSubCodeKey>
                     <SizeWeightInfo>
                        <MaximumSizeInAlternate Units="C">115</MaximumSizeInAlternate>
                        <MaximumSize Units="I">45</MaximumSize>
                        <MaximumWeightInAlternate Units="K">10</MaximumWeightInAlternate>
                        <MaximumWeight Units="L">22</MaximumWeight>
                     </SizeWeightInfo>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="5" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <CommercialNameofBaggageItemType>OVER70LB 32KG BAGGAGE</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="7X">
                        <Text>OVER 70 POUNDS/32 KILOGRAMS</Text>
                     </DescriptionOne>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0ESAEDL</ExtendedSubCodeKey>
                     <SizeWeightInfo>
                        <MinimumWeightInAlternate Units="K">32</MinimumWeightInAlternate>
                        <MinimumWeight Units="L">70</MinimumWeight>
                     </SizeWeightInfo>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="6" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="SP">
                        <Text>SPORTING EQUIPMENT</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>POLE VAULT EQUIPMENT</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="PV">
                        <Text>POLE VAULT EQUIPMENT</Text>
                     </DescriptionOne>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0F3AEDL</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="7" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="SP">
                        <Text>SPORTING EQUIPMENT</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>CANOE KAYAK OARS</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="CK">
                        <Text>CANOE/KAYAK</Text>
                     </DescriptionOne>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0FTAEDL</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="8" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <CommercialNameofBaggageItemType>UPTO50LB 23KG AND62LI 158LCM</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="23">
                        <Text>UP TO 50 POUNDS/23 KILOGRAMS</Text>
                     </DescriptionOne>
                     <DescriptionTwo Code="6U">
                        <Text>UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                     </DescriptionTwo>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0GOACDL</ExtendedSubCodeKey>
                     <SizeWeightInfo>
                        <MaximumSizeInAlternate Units="C">158</MaximumSizeInAlternate>
                        <MaximumSize Units="I">62</MaximumSize>
                        <MaximumWeightInAlternate Units="K">23</MaximumWeightInAlternate>
                        <MaximumWeight Units="L">50</MaximumWeight>
                     </SizeWeightInfo>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="9" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="CY">
                        <Text>CARRY ON HAND
BAGGAGE</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>CARRY ON HAND BAGGAGE</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0L5ACDL</ExtendedSubCodeKey>
                     <RFIC>C</RFIC>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="10" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="CY">
                        <Text>CARRY ON HAND BAGGAGE</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>CARRYON HAND BAGGAGE ALLOWANCE</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0LNABDL</ExtendedSubCodeKey>
                     <RFIC>C</RFIC>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="11" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="CY">
                        <Text>CARRY ON HAND BAGGAGE</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>CARRY ON UP TO 45 LI 115 LCM</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="4U">
                        <Text>UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                     </DescriptionOne>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0MUACDL</ExtendedSubCodeKey>
                     <RFIC>C</RFIC>
                     <SizeWeightInfo>
                        <MaximumSizeInAlternate Units="C">115</MaximumSizeInAlternate>
                        <MaximumSize Units="I">45</MaximumSize>
                     </SizeWeightInfo>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="12" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="CY">
                        <Text>CARRY ON HAND BAGGAGE</Text>
                     </AncillaryService>
                     <CommercialNameofBaggageItemType>CARRYON HAND
BAGGAGE ALLOWANCE</CommercialNameofBaggageItemType>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0LNABAF</ExtendedSubCodeKey>
                  </SubCodeProperties>
                  <SubCodeProperties RPH="13" SolutionSequenceNmbr="1">
                     <AncillaryFeeGroupCode>BG</AncillaryFeeGroupCode>
                     <AncillaryService SubGroupCode="CY">
                        <Text>CARRY ON HAND BAGGAGE</Text>
                     </AncillaryService>
                     <BookingMethod>04</BookingMethod>
                     <CommercialNameofBaggageItemType>CABIN BAGGAGE 12KG 1PC 115CM</CommercialNameofBaggageItemType>
                     <DescriptionOne Code="12">
                        <Text>UP TO 26 POUNDS/12 KILOGRAMS</Text>
                     </DescriptionOne>
                     <DescriptionTwo Code="4U">
                        <Text>UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                     </DescriptionTwo>
                     <EMD_Type>4</EMD_Type>
                     <ExtendedSubCodeKey>0MRACAF</ExtendedSubCodeKey>
                     <SizeWeightInfo>
                        <MaximumSizeInAlternate Units="C">115</MaximumSizeInAlternate>
                        <MaximumSize Units="I">45</MaximumSize>
                        <MaximumWeightInAlternate Units="K">12</MaximumWeightInAlternate>
                        <MaximumWeight Units="L">26</MaximumWeight>
                     </SizeWeightInfo>
                  </SubCodeProperties>
               </BaggageInfo>
               <HeaderInformation SolutionSequenceNmbr="1">
                  <DepartureDate>2019-09-02</DepartureDate>
                  <LastTicketingDate>08-23T23:59</LastTicketingDate>
                  <Text>WHEN TICKETING FOP MUST NOT BE GTR</Text>
                  <Text>PRIVATE FARE APPLIED - CHECK RULES FOR CORRECT TICKETING</Text>
                  <Text>VALIDATING CARRIER - DL</Text>
                  <Text>BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                  <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                  <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON ALLOWANCE</Text>
                  <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                  <Text>01/CARRY ON HAND BAGGAGE</Text>
                  <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                  <Text>CDGDSS-01P/AF</Text>
                  <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                  <Text>LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON CHARGES</Text>
                  <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                  <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/</Text>
                  <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                  <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                  <Text>DTWCDG-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>DSSJFK-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>PET IN CABIN NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>LGADTW-DL</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>PRIVATE \xc2\xa4</Text>
                  <Text>WHEN TICKETING FOP MUST NOT BE GTR</Text>
                  <Text>EACH J11 REQUIRES ACCOMPANYING SAME CABIN JCB</Text>
                  <Text>PRIVATE FARE APPLIED - CHECK RULES FOR CORRECT TICKETING</Text>
                  <Text>VALIDATING CARRIER - DL</Text>
                  <Text>BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                  <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                  <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON ALLOWANCE</Text>
                  <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                  <Text>01/CARRY ON HAND BAGGAGE</Text>
                  <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                  <Text>CDGDSS-01P/AF</Text>
                  <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                  <Text>LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON CHARGES</Text>
                  <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                  <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/</Text>
                  <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                  <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                  <Text>DTWCDG-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>OVER 70 POUNDS/32
KILOGRAMS NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>DSSJFK-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>PET IN CABIN NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>LGADTW-DL</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>PRIVATE \xc2\xa4</Text>
                  <Text>REQUIRES ACCOMPANYING ADT PASSENGER</Text>
                  <Text>WHEN TICKETING FOP MUST NOT BE GTR</Text>
                  <Text>PRIVATE FARE APPLIED - CHECK RULES FOR CORRECT TICKETING</Text>
                  <Text>EACH INF REQUIRES ACCOMPANYING ADT PASSENGER</Text>
                  <Text>VALIDATING CARRIER - DL</Text>
                  <Text>BAG ALLOWANCE     -DTWDSS-01P/DL/EACH PIECE UP TO 22 POUNDS/10</Text>
                  <Text>KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                  <Text>2NDCHECKED BAG FEE-DTWDSS-USD200.00/DL/UP TO 50 POUNDS/23 KILOG</Text>
                  <Text>RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>BAG ALLOWANCE     -DSSDTW-01P/DL/EACH PIECE UP TO 22 POUNDS/10</Text>
                  <Text>KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                  <Text>2NDCHECKED BAG FEE-DSSDTW-USD200.00/DL/UP TO 50 POUNDS/23 KILOG</Text>
                  <Text>RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON ALLOWANCE</Text>
                  <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                  <Text>01/CARRY ON HAND BAGGAGE</Text>
                  <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                  <Text>CDGDSS-01P/AF</Text>
                  <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                  <Text>LINEAR CENTIMETERS</Text>
                  <Text>CARRY ON CHARGES</Text>
                  <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                  <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                  <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER
STATUS/MILITARY/</Text>
                  <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                  <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                  <Text>DTWCDG-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>DSSJFK-DL</Text>
                  <Text>PET IN HOLD NOT PERMITTED</Text>
                  <Text>PET IN CABIN NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>LGADTW-DL</Text>
                  <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                  <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                  <Text>PRIVATE \xc2\xa4</Text>
                  <Text>ELECTRONIC TICKETING NOT VALID FOR INFANTS</Text>
                  <Text>02SEP DEPARTURE DATE-----LAST DAY TO PURCHASE 23AUG/2359</Text>
                  <ValidatingCarrier Code="DL" />
               </HeaderInformation>
               <SolutionInformation SolutionSequenceNmbr="1">
                  <BaseFareCurrencyCode>USD</BaseFareCurrencyCode>
                  <CurrencyCode>USD</CurrencyCode>
                  <GrandTotalEquivFareAmount>2630.00</GrandTotalEquivFareAmount>
                  <GrandTotalTaxes>1804.02</GrandTotalTaxes>
                  <RequiresRebook>false</RequiresRebook>
                  <TicketNumber>0</TicketNumber>
                  <TotalAmount>4434.02</TotalAmount>
               </SolutionInformation>
               <ValidatingCarrier NewValidatingProcess="true" SolutionSequenceNmbr="1">
                  <SettlementMethod>ARC</SettlementMethod>
                  <Ticket CarrierCode="DL" Type="ETKTREQ" ValidatingCarrierType="Default">
                     <InterlineAgreement CarrierCode="AF" Type="3PT" />
                  </Ticket>
               </ValidatingCarrier>
            </MiscInformation>
            <PricedItinerary AlternativePricing="false" CurrencyCode="USD" MultiTicket="false" TotalAmount="4434.02">
               <AirItineraryPricingInfo SolutionSequenceNmbr="1">
                  <BaggageProvisions RPH="1">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="DSS" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">8410</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="CDG" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>2</NumPiecesBDI>
                     <NumPiecesITR>2</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0GOACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="2">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <DestinationLocation LocationCode="DTW" RPH="2" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <FlightNumber RPH="2">955</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <OriginLocation LocationCode="LGA" RPH="2" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <PNR_Segment RPH="2">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>2</NumPiecesBDI>
                     <NumPiecesITR>2</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0GOACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="3">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0L5ACDL</SubCodeForAllowance>
                        <SubCodeForAllowance RPH="2">0MUACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="4">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="DSS" RPH="1" />
                        <FlightNumber RPH="1">8410</FlightNumber>
                        <OriginLocation LocationCode="CDG" RPH="1" />
                        <PNR_Segment RPH="1">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>AF</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0MRACAF</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABAF</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="5">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JCB" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BSAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="6">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JCB" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0ESAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="7">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JCB" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0F3AEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="8">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JCB" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0FTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="9">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JCB" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <FareCalculation>
                     <Text>DTT DL X/E/PAR DL DKR Q DTTDKR4.50M458.00DL X/NYC DL DTT M458.00NUC920.50END ROE1.00 XFDTW4.5LGA4.5</Text>
                  </FareCalculation>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DTW" ArrivalAirportCode="CDG" ArrivalCityCode="PAR" CityCode="DTT" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage ExtraAllowanceInd="E" />
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="CDG" ArrivalAirportCode="DSS" ArrivalCityCode="DKR" CityCode="PAR" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6/LN610" FareAmount="458.00" FarePassengerType="JCB" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DSS" ArrivalAirportCode="JFK" ArrivalCityCode="NYC" CityCode="DKR" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="LGA" ArrivalAirportCode="DTW" ArrivalCityCode="DTT" CityCode="NYC" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6/LN610" FareAmount="458.00" FarePassengerType="JCB" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <ItinTotalFare NonRefundableInd="N">
                     <BaggageInfo>
                        <US_DOT_Disclosure>
                           <Text>BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                           <Text>KILOGRAMS
AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                           <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON ALLOWANCE</Text>
                           <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                           <Text>01/CARRY ON HAND BAGGAGE</Text>
                           <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                           <Text>CDGDSS-01P/AF</Text>
                           <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                           <Text>LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON CHARGES</Text>
                           <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                           <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/</Text>
                           <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                           <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                           <Text>DTWCDG-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>DSSJFK-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>PET IN CABIN NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>LGADTW-DL</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                        </US_DOT_Disclosure>
                     </BaggageInfo>
                     <BaseFare Amount="921.00" CurrencyCode="USD" />
                     <Construction Amount="920.50" CurrencyCode="NUC" RateOfExchange="1.000000" />
                     <Endorsements>
                        <Text>NONEND/NONREF/L-9882/LN610</Text>
                     </Endorsements>
                     <PrivateFare Ind="@" />
                     <Taxes TotalAmount="579.63">
                        <Tax Amount="356.00" TaxCode="YRI" TaxName="SERVICE FEE - CARRIER-IMPOSED" TicketingTaxCode="YR" />
                        <Tax Amount="37.20" TaxCode="US2" TaxName="TRANSPORTATION TAX INTERNATION" TicketingTaxCode="US" />
                        <Tax Amount="5.77" TaxCode="YC" TaxName="CUSTOMS USER FEE" TicketingTaxCode="YC" />
                        <Tax Amount="7.00" TaxCode="XY2" TaxName="IMMIGRATION USER FEE" TicketingTaxCode="XY" />
                        <Tax Amount="3.96" TaxCode="XA" TaxName="APHIS PASSENGER FEE PASSENGERS" TicketingTaxCode="XA" />
                        <Tax Amount="11.20" TaxCode="AY" TaxName="PASSENGER CIVIL AVIATION SECUR" TicketingTaxCode="AY" />
                        <Tax Amount="5.20" TaxCode="FR7" TaxName="AIRPORT TAX DOMESTIC AND INTER" TicketingTaxCode="FR" />
                        <Tax Amount="21.50" TaxCode="QX" TaxName="PASSENGER SERVICE CHARGE INTER" TicketingTaxCode="QX" />
                        <Tax Amount="16.90" TaxCode="DF" TaxName="SECURITY CHARGE INTERNATIONAL" TicketingTaxCode="DF" />
                        <Tax Amount="16.90" TaxCode="ZE" TaxName="PASSENGER SERVICE CHARGE" TicketingTaxCode="ZE" />
                        <Tax Amount="59.90" TaxCode="HP" TaxName="INFRASTRUCTURE DEVELOPMENT CHA" TicketingTaxCode="HP" />
                        <Tax Amount="5.10" TaxCode="KQ" TaxName="CIVIL AVIATION CHARGE" TicketingTaxCode="KQ" />
                        <Tax Amount="24.00" TaxCode="VH" TaxName="IMMIGRATION USER FEE DEPARTURE" TicketingTaxCode="VH" />
                        <Tax Amount="9.00" TaxCode="XF" TaxName="PASSENGER FACILITY CHARGE" TicketingTaxCode="XF" />
                     </Taxes>
                     <TotalFare Amount="1500.63" CurrencyCode="USD" />
                     <Warnings>
                        <Warning ShortText="BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23" />
                        <Warning ShortText="KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23" />
                        <Warning ShortText="KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON ALLOWANCE" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-01P/DL" />
                        <Warning ShortText="01/CARRY ON HAND BAGGAGE" />
                        <Warning ShortText="01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS" />
                        <Warning ShortText="CDGDSS-01P/AF" />
                        <Warning ShortText="01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115" />
                        <Warning ShortText="LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON CHARGES" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON" />
                        <Warning ShortText="FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/" />
                        <Warning ShortText="CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./" />
                        <Warning ShortText="EMBARGOES-APPLY TO EACH PASSENGER" />
                        <Warning ShortText="DTWCDG-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="DSSJFK-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="PET IN CABIN NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="LGADTW-DL" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="MIXED PASSENGER TYPES - VERIFY RESTRICTIONS" />
                     </Warnings>
                  </ItinTotalFare>
                  <PassengerTypeQuantity Code="JCB" Quantity="2" />
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6/LN610" FareAmount="458.00" FarePassengerType="JCB" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6/LN610" FareAmount="458.00" FarePassengerType="JCB" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
               </AirItineraryPricingInfo>
               <AirItineraryPricingInfo SolutionSequenceNmbr="1">
                  <BaggageProvisions RPH="1">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="DSS" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">8410</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="CDG" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>2</NumPiecesBDI>
                     <NumPiecesITR>2</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0GOACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="2">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <DestinationLocation LocationCode="DTW" RPH="2" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <FlightNumber RPH="2">955</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <OriginLocation LocationCode="LGA" RPH="2" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <PNR_Segment RPH="2">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>2</NumPiecesBDI>
                     <NumPiecesITR>2</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0GOACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="3">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0L5ACDL</SubCodeForAllowance>
                        <SubCodeForAllowance RPH="2">0MUACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="4">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="DSS" RPH="1" />
                        <FlightNumber RPH="1">8410</FlightNumber>
                        <OriginLocation LocationCode="CDG" RPH="1" />
                        <PNR_Segment RPH="1">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>AF</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0MRACAF</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABAF</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="5">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNN" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BSAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="6">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNN" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0ESAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="7">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNN" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0F3AEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="8">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNN" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0FTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="9">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNN" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <FareCalculation>
                     <Text>DTT DL X/E/PAR DL DKR Q DTTDKR4.50M343.50DL X/NYC DL DTT M343.50NUC691.50END ROE1.00 XFDTW4.5LGA4.5</Text>
                  </FareCalculation>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DTW" ArrivalAirportCode="CDG" ArrivalCityCode="PAR" CityCode="DTT" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6C/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage ExtraAllowanceInd="E" />
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="CDG" ArrivalAirportCode="DSS" ArrivalCityCode="DKR" CityCode="PAR" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6C/LN610" FareAmount="343.50" FarePassengerType="J11" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>19</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DSS" ArrivalAirportCode="JFK" ArrivalCityCode="NYC" CityCode="DKR" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6C/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="LGA" ArrivalAirportCode="DTW" ArrivalCityCode="DTT" CityCode="NYC" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6C/LN610" FareAmount="343.50" FarePassengerType="J11" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>19</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <ItinTotalFare NonRefundableInd="N">
                     <BaggageInfo>
                        <US_DOT_Disclosure>
                           <Text>BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                           <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23</Text>
                           <Text>KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON ALLOWANCE</Text>
                           <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                           <Text>01/CARRY ON HAND BAGGAGE</Text>
                           <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                           <Text>CDGDSS-01P/AF</Text>
                           <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                           <Text>LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON CHARGES</Text>
                           <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                           <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/</Text>
                           <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                           <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                           <Text>DTWCDG-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>DSSJFK-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>PET IN CABIN NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>LGADTW-DL</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                        </US_DOT_Disclosure>
                     </BaggageInfo>
                     <BaseFare Amount="692.00" CurrencyCode="USD" />
                     <Construction Amount="691.50" CurrencyCode="NUC" RateOfExchange="1.000000" />
                     <Endorsements>
                        <Text>NONEND/NONREF/L-9882/LN610</Text>
                     </Endorsements>
                     <PrivateFare Ind="@" />
                     <Taxes TotalAmount="579.63">
                        <Tax Amount="356.00" TaxCode="YRI" TaxName="SERVICE FEE - CARRIER-IMPOSED" TicketingTaxCode="YR" />
                        <Tax Amount="37.20" TaxCode="US2" TaxName="TRANSPORTATION TAX INTERNATION" TicketingTaxCode="US" />
                        <Tax Amount="5.77" TaxCode="YC" TaxName="CUSTOMS USER FEE" TicketingTaxCode="YC" />
                        <Tax Amount="7.00" TaxCode="XY2" TaxName="IMMIGRATION USER FEE" TicketingTaxCode="XY" />
                        <Tax Amount="3.96" TaxCode="XA" TaxName="APHIS PASSENGER FEE PASSENGERS" TicketingTaxCode="XA" />
                        <Tax Amount="11.20" TaxCode="AY" TaxName="PASSENGER CIVIL AVIATION SECUR" TicketingTaxCode="AY" />
                        <Tax Amount="5.20" TaxCode="FR7" TaxName="AIRPORT TAX DOMESTIC AND INTER" TicketingTaxCode="FR" />
                        <Tax Amount="21.50" TaxCode="QX" TaxName="PASSENGER SERVICE CHARGE INTER" TicketingTaxCode="QX" />
                        <Tax Amount="16.90" TaxCode="DF" TaxName="SECURITY CHARGE INTERNATIONAL" TicketingTaxCode="DF" />
                        <Tax Amount="16.90" TaxCode="ZE" TaxName="PASSENGER SERVICE CHARGE" TicketingTaxCode="ZE" />
                        <Tax Amount="59.90" TaxCode="HP" TaxName="INFRASTRUCTURE DEVELOPMENT CHA" TicketingTaxCode="HP" />
                        <Tax Amount="5.10" TaxCode="KQ" TaxName="CIVIL AVIATION CHARGE" TicketingTaxCode="KQ" />
                        <Tax Amount="24.00" TaxCode="VH" TaxName="IMMIGRATION USER FEE DEPARTURE" TicketingTaxCode="VH" />
                        <Tax Amount="9.00" TaxCode="XF" TaxName="PASSENGER FACILITY CHARGE" TicketingTaxCode="XF" />
                     </Taxes>
                     <TotalFare Amount="1271.63" CurrencyCode="USD" />
                     <Warnings>
                        <Warning ShortText="BAG ALLOWANCE     -DTWDSS-02P/DL/EACH PIECE UP TO 50 POUNDS/23" />
                        <Warning ShortText="KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="BAG ALLOWANCE     -DSSDTW-02P/DL/EACH PIECE UP TO 50 POUNDS/23" />
                        <Warning ShortText="KILOGRAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON ALLOWANCE" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-01P/DL" />
                        <Warning ShortText="01/CARRY ON HAND BAGGAGE" />
                        <Warning ShortText="01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS" />
                        <Warning ShortText="CDGDSS-01P/AF" />
                        <Warning ShortText="01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115" />
                        <Warning ShortText="LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON CHARGES" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON" />
                        <Warning ShortText="FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/" />
                        <Warning ShortText="CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./" />
                        <Warning ShortText="EMBARGOES-APPLY TO EACH PASSENGER" />
                        <Warning ShortText="DTWCDG-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="DSSJFK-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="PET IN CABIN NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="LGADTW-DL" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="MIXED PASSENGER TYPES - VERIFY RESTRICTIONS" />
                     </Warnings>
                  </ItinTotalFare>
                  <PassengerTypeQuantity Code="J11" Quantity="1" />
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6C/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6C/LN610" FareAmount="343.50" FarePassengerType="J11" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6C/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6C/LN610" FareAmount="343.50" FarePassengerType="J11" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC002</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
               </AirItineraryPricingInfo>
               <AirItineraryPricingInfo SolutionSequenceNmbr="1">
                  <BaggageProvisions RPH="1">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="DSS" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">8410</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="CDG" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0E3ACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="2">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="DSS" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">8410</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="CDG" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeApplicationIndicator>4</FeeApplicationIndicator>
                     <FeeNotGuaranteedIndicator>N</FeeNotGuaranteedIndicator>
                     <FirstOccurrence>1</FirstOccurrence>
                     <Interlineable>Y</Interlineable>
                     <LastOccurrence>8</LastOccurrence>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="200.00" CurrencyCode="USD" />
                        <Equiv Amount="200.00" CurrencyCode="USD" />
                        <TaxIndicator>X</TaxIndicator>
                        <Total>200.00</Total>
                     </PriceInformation>
                     <ProvisionType>C</ProvisionType>
                     <RefundReissue>N</RefundReissue>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0GOACDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="3">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <DestinationLocation LocationCode="DTW" RPH="2" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <FlightNumber RPH="2">955</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <OriginLocation LocationCode="LGA" RPH="2" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <PNR_Segment RPH="2">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>A</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0E3ACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0DFAADL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="4">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <DestinationLocation LocationCode="DTW" RPH="2" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <FlightNumber RPH="2">955</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <OriginLocation LocationCode="LGA" RPH="2" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <PNR_Segment RPH="2">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeApplicationIndicator>4</FeeApplicationIndicator>
                     <FeeNotGuaranteedIndicator>N</FeeNotGuaranteedIndicator>
                     <FirstOccurrence>1</FirstOccurrence>
                     <Interlineable>Y</Interlineable>
                     <LastOccurrence>8</LastOccurrence>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="200.00" CurrencyCode="USD" />
                        <Equiv Amount="200.00" CurrencyCode="USD" />
                        <TaxIndicator>X</TaxIndicator>
                        <Total>200.00</Total>
                     </PriceInformation>
                     <ProvisionType>C</ProvisionType>
                     <RefundReissue>N</RefundReissue>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0GOACDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="5">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0L5ACDL</SubCodeForAllowance>
                        <SubCodeForAllowance RPH="2">0MUACDL</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="6">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-03</DepartureDate>
                        <DestinationLocation LocationCode="DSS" RPH="1" />
                        <FlightNumber RPH="1">8410</FlightNumber>
                        <OriginLocation LocationCode="CDG" RPH="1" />
                        <PNR_Segment RPH="1">3</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>AF</CarrierWhoseBaggageProvisionsApply>
                     <NumPiecesBDI>1</NumPiecesBDI>
                     <NumPiecesITR>1</NumPiecesITR>
                     <ProvisionType>B</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForAllowance RPH="1">0MRACAF</SubCodeForAllowance>
                        <SubCodeForChargesOthers>0LNABAF</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="7">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CountForSegmentAssociatedID>2</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BSAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="8">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0ESAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="9">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0F3AEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="10">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CarrierCode RPH="2">DL</CarrierCode>
                        <CarrierCode RPH="3">DL</CarrierCode>
                        <CountForSegmentAssociatedID>3</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-02</DepartureDate>
                        <DepartureDate RPH="2">2019-09-19</DepartureDate>
                        <DepartureDate RPH="3">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="CDG" RPH="1" />
                        <DestinationLocation LocationCode="JFK" RPH="2" />
                        <DestinationLocation LocationCode="DTW" RPH="3" />
                        <FlightNumber RPH="1">96</FlightNumber>
                        <FlightNumber RPH="2">217</FlightNumber>
                        <FlightNumber RPH="3">955</FlightNumber>
                        <OriginLocation LocationCode="DTW" RPH="1" />
                        <OriginLocation LocationCode="DSS" RPH="2" />
                        <OriginLocation LocationCode="LGA" RPH="3" />
                        <PNR_Segment RPH="1">2</PNR_Segment>
                        <PNR_Segment RPH="2">4</PNR_Segment>
                        <PNR_Segment RPH="3">5</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="2">T</ResBookDesigCode>
                        <ResBookDesigCode RPH="3">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                        <StatusCode RPH="2">HK</StatusCode>
                        <StatusCode RPH="3">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0FTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <BaggageProvisions RPH="11">
                     <Associations>
                        <CarrierCode RPH="1">DL</CarrierCode>
                        <CountForSegmentAssociatedID>1</CountForSegmentAssociatedID>
                        <DepartureDate RPH="1">2019-09-19</DepartureDate>
                        <DestinationLocation LocationCode="JFK" RPH="1" />
                        <FlightNumber RPH="1">217</FlightNumber>
                        <OriginLocation LocationCode="DSS" RPH="1" />
                        <PNR_Segment RPH="1">4</PNR_Segment>
                        <ResBookDesigCode RPH="1">T</ResBookDesigCode>
                        <StatusCode RPH="1">HK</StatusCode>
                     </Associations>
                     <CarrierWhoseBaggageProvisionsApply>DL</CarrierWhoseBaggageProvisionsApply>
                     <Commissionable>N</Commissionable>
                     <FeeNotGuaranteedIndicator>Y</FeeNotGuaranteedIndicator>
                     <NoChargeNotAvailableIndicator>X</NoChargeNotAvailableIndicator>
                     <PassengerType Code="JNF" />
                     <PriceInformation>
                        <Base Amount="0.00" />
                        <Equiv CurrencyCode="USD" />
                     </PriceInformation>
                     <ProvisionType>E</ProvisionType>
                     <SubCodeInfo>
                        <SubCodeForChargesOthers>0BTAEDL</SubCodeForChargesOthers>
                     </SubCodeInfo>
                  </BaggageProvisions>
                  <FareCalculation>
                     <Text>DTT DL X/E/PAR DL DKR Q DTTDKR4.50M45.80DL X/NYC DL DTT M45.80NUC96.10END ROE1.00</Text>
                  </FareCalculation>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DTW" ArrivalAirportCode="CDG" ArrivalCityCode="PAR" CityCode="DTT" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6I/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                     <Mileage ExtraAllowanceInd="E" />
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="CDG" ArrivalAirportCode="DSS" ArrivalCityCode="DKR" CityCode="PAR" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6I/LN610" FareAmount="45.80" FarePassengerType="JNF" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>19</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Departure AirlineCode="DL" AirportCode="DSS" ArrivalAirportCode="JFK" ArrivalCityCode="NYC" CityCode="DKR" GenericInd="X" />
                     <FareBasis Cabin="Y" Code="TK1H00M6I/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                  </FareCalculationBreakdown>
                  <FareCalculationBreakdown>
                     <Branch FirstJointCarrier="DL" PCC="WR17" />
                     <Departure AirlineCode="DL" AirportCode="LGA" ArrivalAirportCode="DTW" ArrivalCityCode="DTT" CityCode="NYC" GenericInd="O" />
                     <FareBasis Cabin="Y" Code="TK1H00M6I/LN610" FareAmount="45.80" FarePassengerType="JNF" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" TripTypeInd="R" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                     <Mileage MileageSymbol="M" />
                     <RuleCategoryIndicator>1</RuleCategoryIndicator>
                     <RuleCategoryIndicator>4</RuleCategoryIndicator>
                     <RuleCategoryIndicator>8</RuleCategoryIndicator>
                     <RuleCategoryIndicator>10</RuleCategoryIndicator>
                     <RuleCategoryIndicator>15</RuleCategoryIndicator>
                     <RuleCategoryIndicator>16</RuleCategoryIndicator>
                     <RuleCategoryIndicator>18</RuleCategoryIndicator>
                     <RuleCategoryIndicator>19</RuleCategoryIndicator>
                     <RuleCategoryIndicator>25</RuleCategoryIndicator>
                     <RuleCategoryIndicator>35</RuleCategoryIndicator>
                  </FareCalculationBreakdown>
                  <ItinTotalFare NonRefundableInd="N">
                     <BaggageInfo>
                        <US_DOT_Disclosure>
                           <Text>BAG ALLOWANCE     -DTWDSS-01P/DL/EACH PIECE UP TO 22 POUNDS/10</Text>
                           <Text>KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                           <Text>2NDCHECKED BAG FEE-DTWDSS-USD200.00/DL/UP TO 50 POUNDS/23 KILOG</Text>
                           <Text>RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>BAG ALLOWANCE     -DSSDTW-01P/DL/EACH PIECE UP TO 22 POUNDS/10</Text>
                           <Text>KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                           <Text>2NDCHECKED BAG FEE-DSSDTW-USD200.00/DL/UP TO 50 POUNDS/23 KILOG</Text>
                           <Text>RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON ALLOWANCE</Text>
                           <Text>DTWCDG DSSJFK LGADTW-01P/DL</Text>
                           <Text>01/CARRY ON HAND BAGGAGE</Text>
                           <Text>01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS</Text>
                           <Text>CDGDSS-01P/AF</Text>
                           <Text>01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115</Text>
                           <Text>LINEAR CENTIMETERS</Text>
                           <Text>CARRY ON CHARGES</Text>
                           <Text>DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER</Text>
                           <Text>ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON</Text>
                           <Text>FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/</Text>
                           <Text>CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./</Text>
                           <Text>EMBARGOES-APPLY TO EACH PASSENGER</Text>
                           <Text>DTWCDG-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>DSSJFK-DL</Text>
                           <Text>PET IN HOLD NOT PERMITTED</Text>
                           <Text>PET IN CABIN NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                           <Text>LGADTW-DL</Text>
                           <Text>SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED</Text>
                           <Text>SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED</Text>
                        </US_DOT_Disclosure>
                     </BaggageInfo>
                     <BaseFare Amount="96.00" CurrencyCode="USD" />
                     <Construction Amount="96.10" CurrencyCode="NUC" RateOfExchange="1.000000" />
                     <Endorsements>
                        <Text>NONEND/NONREF/L-9882/LN610</Text>
                     </Endorsements>
                     <PrivateFare Ind="@" />
                     <Taxes TotalAmount="65.13">
                        <Tax Amount="37.20" TaxCode="US2" TaxName="TRANSPORTATION TAX INTERNATION" TicketingTaxCode="US" />
                        <Tax Amount="5.77" TaxCode="YC" TaxName="CUSTOMS USER FEE" TicketingTaxCode="YC" />
                        <Tax Amount="7.00" TaxCode="XY2" TaxName="IMMIGRATION USER FEE" TicketingTaxCode="XY" />
                        <Tax Amount="3.96" TaxCode="XA" TaxName="APHIS PASSENGER FEE PASSENGERS" TicketingTaxCode="XA" />
                        <Tax Amount="11.20" TaxCode="AY" TaxName="PASSENGER CIVIL AVIATION SECUR" TicketingTaxCode="AY" />
                     </Taxes>
                     <TotalFare Amount="161.13" CurrencyCode="USD" />
                     <Warnings>
                        <Warning ShortText="BAG ALLOWANCE     -DTWDSS-01P/DL/EACH PIECE UP TO 22 POUNDS/10" />
                        <Warning ShortText="KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS" />
                        <Warning ShortText="2NDCHECKED BAG FEE-DTWDSS-USD200.00/DL/UP TO 50 POUNDS/23 KILOG" />
                        <Warning ShortText="RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="BAG ALLOWANCE     -DSSDTW-01P/DL/EACH PIECE UP TO 22 POUNDS/10" />
                        <Warning ShortText="KILOGRAMS AND UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS" />
                        <Warning ShortText="2NDCHECKED BAG FEE-DSSDTW-USD200.00/DL/UP TO 50 POUNDS/23 KILOG" />
                        <Warning ShortText="RAMS AND UP TO 62 LINEAR INCHES/158 LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON ALLOWANCE" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-01P/DL" />
                        <Warning ShortText="01/CARRY ON HAND BAGGAGE" />
                        <Warning ShortText="01/UP TO 45 LINEAR INCHES/115 LINEAR CENTIMETERS" />
                        <Warning ShortText="CDGDSS-01P/AF" />
                        <Warning ShortText="01/UP TO 26 POUNDS/12 KILOGRAMS AND UP TO 45 LINEAR INCHES/115" />
                        <Warning ShortText="LINEAR CENTIMETERS" />
                        <Warning ShortText="CARRY ON CHARGES" />
                        <Warning ShortText="DTWCDG DSSJFK LGADTW-DL-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="CDGDSS-AF-CARRY ON FEES UNKNOWN-CONTACT CARRIER" />
                        <Warning ShortText="ADDITIONAL ALLOWANCES AND/OR DISCOUNTS MAY APPLY DEPENDING ON" />
                        <Warning ShortText="FLYER-SPECIFIC FACTORS /E.G. FREQUENT FLYER STATUS/MILITARY/" />
                        <Warning ShortText="CREDIT CARD FORM OF PAYMENT/EARLY PURCHASE OVER INTERNET,ETC./" />
                        <Warning ShortText="EMBARGOES-APPLY TO EACH PASSENGER" />
                        <Warning ShortText="DTWCDG-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="OVER 70 POUNDS/32 KILOGRAMS NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="DSSJFK-DL" />
                        <Warning ShortText="PET IN HOLD NOT PERMITTED" />
                        <Warning ShortText="PET IN CABIN NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="LGADTW-DL" />
                        <Warning ShortText="SPORTING EQUIPMENT/POLE VAULT EQUIPMENT NOT PERMITTED" />
                        <Warning ShortText="SPORTING EQUIPMENT/CANOE/KAYAK NOT PERMITTED" />
                        <Warning ShortText="MIXED PASSENGER TYPES - VERIFY RESTRICTIONS" />
                     </Warnings>
                  </ItinTotalFare>
                  <PassengerTypeQuantity Code="JNF" Quantity="1" />
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6I/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                     <Surcharges Ind="Q" Type="UNK">4.50</Surcharges>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6I/LN610" FareAmount="45.80" FarePassengerType="JNF" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6I/LN610" FilingCarrier="DL" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
                  <PTC_FareBreakdown>
                     <Cabin>Y</Cabin>
                     <FareBasis Code="TK1H00M6I/LN610" FareAmount="45.80" FarePassengerType="JNF" FareType="N" FilingCarrier="DL" GlobalInd="AT" Market="DTTDKR" TicketDesignator="LN610" />
                     <FreeBaggageAllowance>PC001</FreeBaggageAllowance>
                  </PTC_FareBreakdown>
               </AirItineraryPricingInfo>
            </PricedItinerary>
         </PriceQuote>
      </OTA_AirPriceRS>
   </soap-env:Body>
</soap-env:Envelope>"""

r = {
    "status": "Complete",
    "air_itinerary_pricing_info": [
        {
            "base_fare": "921.00",
            "taxes": "579.63",
            "total_fare": "1500.63",
            "currency_code": "USD",
            "passenger_type": "JCB",
            "passenger_quantity": "2",
            "charge_amount": "1500.63",
            "tour_code": None,
            "ticket_designator": None,
            "commission_percentage": 0,
            "fare_break_down": [
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6/LN610",
                    "fare_amount": "458.00",
                    "fare_passenger_type": "JCB",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6/LN610",
                    "fare_amount": "458.00",
                    "fare_passenger_type": "JCB",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6/LN610",
                    "fare_amount": "458.00",
                    "fare_passenger_type": "JCB",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6/LN610",
                    "fare_amount": "458.00",
                    "fare_passenger_type": "JCB",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                }
            ]
        },
        {
            "base_fare": "692.00",
            "taxes": "579.63",
            "total_fare": "1271.63",
            "currency_code": "USD",
            "passenger_type": "J11",
            "passenger_quantity": "1",
            "charge_amount": "1271.63",
            "tour_code": None,
            "ticket_designator": None,
            "commission_percentage": 0,
            "fare_break_down": [
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6C/LN610",
                    "fare_amount": "343.50",
                    "fare_passenger_type": "J11",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6C/LN610",
                    "fare_amount": "343.50",
                    "fare_passenger_type": "J11",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6C/LN610",
                    "fare_amount": "343.50",
                    "fare_passenger_type": "J11",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6C/LN610",
                    "fare_amount": "343.50",
                    "fare_passenger_type": "J11",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                }
            ]
        },
        {
            "base_fare": "96.00",
            "taxes": "65.13",
            "total_fare": "161.13",
            "currency_code": "USD",
            "passenger_type": "JNF",
            "passenger_quantity": "1",
            "charge_amount": "161.13",
            "tour_code": None,
            "ticket_designator": None,
            "commission_percentage": 0,
            "fare_break_down": [
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6I/LN610",
                    "fare_amount": "45.80",
                    "fare_passenger_type": "JNF",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6I/LN610",
                    "fare_amount": "45.80",
                    "fare_passenger_type": "JNF",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6I/LN610",
                    "fare_amount": "45.80",
                    "fare_passenger_type": "JNF",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                },
                {
                    "cabin": "Y",
                    "fare_basis_code": "TK1H00M6I/LN610",
                    "fare_amount": "45.80",
                    "fare_passenger_type": "JNF",
                    "fare_type": "N",
                    "filing_carrier": "DL"
                }
            ]
        }
    ]
}


class ExtractorTest(unittest.TestCase):
    def test_price_search_extractor(self):
        response_extrac = PriceSearchExtractor(xml).extract()
        self.assertIsNotNone(response_extrac.payload)
        self.assertEqual(len(response_extrac.payload.air_itinerary_pricing_info), len(r['air_itinerary_pricing_info']))
        self.assertEqual(response_extrac.payload.status, "Complete")


if __name__ == "__main__":
    unittest.main()
