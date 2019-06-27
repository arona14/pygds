"""BaseService class file"""


class BaseService:
    """Base service class for all sabre classes.
    It initialises the soap URL of the sabre services and the request header.
    """

    def __init__(self):
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}
