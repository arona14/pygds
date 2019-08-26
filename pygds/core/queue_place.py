class QueuePlace():
    """This class is for holding information about queue place
    """
    def __init__(self, status: str = None, type_response: str = None, text_message: str = None):
        self.status = status
        self.type_response = type_response
        self.text_message = text_message

    def to_data(self):
        return {"status": self.status, "type_response": self.type_response, "text_message": self.text_message}
