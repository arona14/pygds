from amadeus.client import AmadeusClient
from env_settings import get_setting


def test():
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")

    client = AmadeusClient(endpoint, username, password, office_id, wsap)
    res = client.start_new_session()
    print(str(res))


if __name__ == "__main__":
    test()
