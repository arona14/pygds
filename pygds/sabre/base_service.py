class BaseService:
    def __init__(self):
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}
