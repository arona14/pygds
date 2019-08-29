class EndTransaction():
    """This class is for holding information about end transaction
    """
    def __init__(self, status: str = None, id_ref: str = None, create_date_time: str = None, text_message: str = None):
        self.status = status
        self.id_ref = id_ref
        self.create_date_time = create_date_time
        self.text_message = text_message

    def to_data(self):
        return {"status": self.status, "id_ref": self.id_ref, "create_date_time": self.create_date_time, "text_message": self.text_message}
