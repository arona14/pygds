from amadeus.client import AmadeusClient


def test():
    client = AmadeusClient()
    res = client.start_new_session()
    print(str(res))


if __name__ == "__main__":
    test()
