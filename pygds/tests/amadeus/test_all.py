from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting


def test():
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")

    client = AmadeusClient(endpoint, username, password, office_id, wsap)
    try:
        session_info = client.start_new_session()
        print(session_info)
        # res = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
        res = client.fare_price_pnr_with_booking_class("WbsConsu-BKqflYaGY0WAgxkCQ00ACBQ20GM3Jit-Yhnyfq1dH", session_info.session_id, "4", session_info.security_token)
        print(str(res))
    except ClientError as ce:
        print(f"client_error: {ce}")
    except ServerError as se:
        print(f"server_error: {se}")


if __name__ == "__main__":
    test()
