from pygds.sabre.json_parsers.revalidate_extract import BaseResponseRevalidateExtractor, RevalidateItinerarieInfo


class RevalidateItinerary(BaseResponseRevalidateExtractor):
    """
    This class retrieves information for revalidate itinerary
    """
    def __init__(self, json_content):
        super().__init__(json_content, main_tag="")

    def _extract(self):
        revalidate_itinerarie = RevalidateItinerarieInfo()
        revalidate_itinerarie.status = ""
        revalidate_itinerarie.brand_feature = []
        revalidate_itinerarie.priced_itinerarie = {}
        revalidate_itinerarie.tpa_extension = {}
        return revalidate_itinerarie
