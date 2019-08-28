class IgnoreTransaction():
    """This class is for holding information about ignore transaction
    """
    def __init__(self, status: str = None, create_date_time: str = None):
        self.status = status
        self.create_date_time = create_date_time

    def to_data(self):
        return {"status": self.status, "create_date_time": self.create_date_time}
