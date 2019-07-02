from amadeus.client import AmadeusClient
from env_settings import get_setting


def test():
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")

    client = AmadeusClient(endpoint, username, password, office_id, wsap)
    # res = client.start_new_session()
    # res = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
    res = client.fare_price_pnr_with_booking_class("WbsConsu-BKqflYaGY0WAgxkCQ00ACBQ20GM3Jit-Yhnyfq1dH", "00DH142EQW", "4", "1F14NTTFP6MZ92O1887SKTVWD6")
    print(str(res))


# if __name__ == "__main__":
#     test()
