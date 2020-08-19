# 0.0.4 (2019-10-22)
- Core
  - remove fake tests [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
- Sabre
  - fix on price [VirginieSy](virginie@ctsfares.com)
  - create PNR with brand [VirginieSy](virginie@ctsfares.com)
  - create PNR [VirginieSy](virginie@ctsfares.com), [mbayane1990](mbaye@ctsfares.com)
  - ticket [VirginieSy](virginie@ctsfares.com), [Mamedemba](demba@ctsfares.com)
  - display PNR [VirginieSy](virginie@ctsfares.com)
  - seat map [Modiao](modou@ctsfares.com)
  - confirm exchange [VirginieSy](virginie@ctsfares.com)
  - price exchange [VirginieSy](virginie@ctsfares.com)
  - extract session [mbayane1990](mbaye@ctsfares.com)
  - update passenger [Modiao](modou@ctsfares.com)
  - close session [mbayane1990](mbaye@ctsfares.com)
  - exchange shopping [VirginieSy](virginie@ctsfares.com)
  - store price [mbayane1990](mbaye@ctsfares.com)
  - rebook air segment [mbayane1990](mbaye@ctsfares.com)
  - exchange [VirginieSy](virginie@ctsfares.com)
  - create PNR [mbayane1990](mbaye@ctsfares.com)
  - ignore transaction [Mamedemba](demba@ctsfares.com)
  - send remark [mbayane1990](mbaye@ctsfares.com)
  - search price [mbayane1990](mbaye@ctsfares.com)
- Amadeus
  - low fare search [salioucts](saliou@ctsfares.com)
  - update passenger [diallocts](amadou@ctsfares.com)
  - create PNR [diallocts](amadou@ctsfares.com)
  - price PNR [diallocts](amadou@ctsfares.com)
  - seat Map [Modiao](modou@ctsfares.com)
  - ticketing [diallocts](amadou@ctsfares.com), [salioucts](saliou@ctsfares.com), [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  - extract PNR info [salioucts](saliou@ctsfares.com)
  - timezone security [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  - extract get reservation [salioucts](saliou@ctsfares.com)
  - store TST [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  - create TST [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  - price segments and passengers [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  - get reservation [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
  
 # 0.0.7 (2019-11-05)
 - Sabre:
    - fix on retrieval of form of payment in get reservation [salioucts](saliou@ctsfares.com)
 
 # 0.0.8 (2019-11-05)
 - Core:
    - abstract class for session handler [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
    
 - Sabre:
    - Revisit session in all methods [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
    
# 0.0.9 (2019-11-06)
- Core:
    - Decorator to handle open and close session [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
- Sabre
    - Remove message ids [mbayane1990](mbaye@ctsfares.com), [Mamedemba](demba@ctsfares.com)
    - Handle expiration date for Rest Tokens [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)

# 0.0.10 (2019-11-07)
- Fix on Sabre seat map extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.11 (2019-11-07)
- Add some methods on Sabre seat map extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.12 (2019-11-13)
- Sabre:
    - Add brands per segment in store price [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)

# 0.0.13 (2019-11-13)
- Sabre:
    - change xml builder on  update passengers request [mbayane1990](mbaye@ctsfares.com)

# 0.0.14 (2019-11-14)
- Sabre:
    - change xml builder on  update passengers request [mbayane1990](mbaye@ctsfares.com)
    
# 0.0.15 (2019-11-14)
- Sabre:
    - fix retrieving tour code and ticket designator if not present [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)

# 0.0.16 (2019-11-14)
- Sabre:
    - fix builder seat_request (sabre seat map request) [mbayane1990](mbaye@ctsfares.com)

# 0.0.17 (2019-11-14)
- Sabre:
    - fest add seat info  to display pnr extractor (passengers & segments) [mbayane1990](mbaye@ctsfares.com)

# 0.0.18 (2019-11-18)
- Sabre:
    - fix on getting infant gender and date of birth [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
    - add application error to seat map extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.19 (2019-11-19)
- Sabre:
    - fix seat info on retreive pnr [mbayane1990](mbaye@ctsfares.com)

# 0.0.20 (2019-11-20)
- Sabre:
    - feat add passengers info to seat map request [mbayane1990](mbaye@ctsfares.com)
    - feat add name assoc id (traveler id) to display pnr extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.22 (2019-11-28)
- Sabre:
    - adding pseudo city code in parameter revalidate[virginieSy](virginie@ctsfares.com)

# 0.0.23 (2019-12-1)
- Core:
    - use jwt as token for amadeus response[diallocts](amadou@ctsfares.com)
- Amadeus:
    - change format of amadeus retrieve pnr as sabre retrieve pnr response[salioucts](saliou@ctsfares.com)
    - change signature of amadeus retrieve pnr as sabre retrieve pnr signature[diallocts](amadou@ctsfares.com)


# 0.0.24 (2019-12-3)
- Sabre:
    - Adding the remark_type parameter in the API allows you to add notes to a pnr[Virginie](virginie@ctsfares.com)

# 0.0.25 (2019-12-4)
- Sabre:
    - change the number of parameters for the forms of payment[Virginie](virginie@ctsfares.com)
    - Adding stop quantity field to retreive pnr extractor [mbayane1990](mbaye@ctsfares.com)


# 0.0.26 (2019-12-4)
- Sabre:
    - Change version to 0.0.26[Virginie](virginie@ctsfares.com)

# 0.0.27 (2019-12-09)
- Sabre:
    - Change seat map request (add operating flight number and marketing flight number) [mbayane1990](mbaye@ctsfares.com)

# 0.0.28 (2019-12-10)
- Sabre:
    - update seat map request (add operating flight number and marketing flight number) [mbayane1990](mbaye@ctsfares.com)

# 0.0.29 (2019-12-13)
- Sabre:
    - update display pnr response extractor for amadeus[Virginie](virginie@ctsfares.com)

# 0.0.30 (2019-12-17)
- Sabre:
    - update seat map request [mbayane1990](mbaye@ctsfares.com)

# 0.0.31 (2019-12-19)
- Sabre:
    - update display pnr extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.32 (2019-12-24)
- Sabre:
    - seat map extractor change replace( BasePrice to Price) [mbayane1990](mbaye@ctsfares.com)

# 0.0.33 (2019-12-31)
- Amadeus:
    - search and store price change replace( fare_price_pnr_with_booking_class to search_price_quote and ticket_create_tst_from_price to store_price_quote) [salioucts](saliou@ctsfares.com)

# 0.0.34 (2020-01-02)
- Amadeus:
    - Integrate commission in search price with fare type Pub [salioucts](saliou@ctsfares.com)

# 0.0.35 (2020-01-07)
- Sabre:
    - Addition of information on penalties in the price search request [VirginieSy](virginie@ctsfares.com)

# 0.0.36 (2020-01-07)
- Sabre:
    - Modification of the request for the creation of pnr, change the format in AirPrice [VirginieSy](virginie@ctsfares.com)

# 0.0.37 (2020-01-07)
- Sabre:
    - In the request for creation of pnr, in AirPrice, modification of the attribute for the ticket designator [VirginieSy]      (virginie@ctsfares.com)
    
# 0.0.38 (2020-01-23)
- Sabre:
    - add info to update passenger builder [mbayane1990](mbaye@ctsfares.com)

# 0.0.39 (2020-01-23)
- Sabre:
    - add info to update store price builder [VirginieSy](virginie@ctsfares.com)

# 0.0.40 (2020-02-04)
- Sabre:
    - Update search price builder [VirginieSy](virginie@ctsfares.com)
    
# 0.0.41 (2020-02-10)
- Sabre:
    - Update display pnr response extractor [mbayane1990](mbaye@ctsfares.com)

# 0.0.42 (2020-04-01)
- Sabre:
    - Implementation of the method allowing to search for new itineraries for the exchange of a ticket number. [VirginieSy](virginie@ctsfares.com)

# 0.0.43 (2020-04-10)
- Sabre:
    - Modifications of responses for the exchange procedure with gds Sable. [VirginieSy](virginie@ctsfares.com)

# 0.0.44 (2020-04-16)
- Sabre:
    - Addition of passenger type in exchange shopping extraction with gds Sabre. [VirginieSy](virginie@ctsfares.com)

# 0.0.45 (2020-04-17)
- Sabre:
    - Modify the extraction of information relating to ticket numbers. [VirginieSy](virginie@ctsfares.com)

# 0.0.46 (2020-04-17)
- Sabre:
    - Modification of the extraction of price quote information from a pnr. [VirginieSy](virginie@ctsfares.com)

# 0.0.47 (2020-04-30)
- Sabre:
    - Modification of the extraction of ticket exchange. [VirginieSy](virginie@ctsfares.com)

# 0.0.48 (2020-06-24)
- Sabre:
    - Modification in the extraction of data for display pnr, by reforming the date of birth. [VirginieSy](virginie@ctsfares.com)
    
# 0.0.49 (2020-07-16)
- Sabre:
    - Update store price Rq builder ( to fixe Tour Code None with commission percent) [mbayane1990](mbaye@ctsfares.com)

# 0.0.50 (2020-07-28)
- Sabre:
    - skip pqs without fare info in Price Quote Services extractor [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
    - get None if cannot match ticket number to passenger on retrieve PNR [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)

# 0.0.51 (2020-08-06)
- Sabre:
    - fix bug introduced in version 0.0.50: skip only pqs without fare info in Price Quote Services extractor [Mouhamad Ndiankho THIAM](mohamed@ctsfares.com)
    
 # 0.0.52 (2020-08-12)
 - Sabre:
     - Update store price Rq builder ( use rph=1 on SegmentSelect and CommandPricing when we haven't brands and do not 
     send penality with CommandPricing ) [mbayane1990](mbaye@ctsfares.com)
     
 # 0.0.53 (2020-08-18)
 - Sabre:
     - Update store price Rq builder ( to avoid RPH Where pax type is Net ) [mbayane1990](mbaye@ctsfares.com)