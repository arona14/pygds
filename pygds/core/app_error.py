class ApplicationError:
    """
    A class to hold information about application error
    """
    def __init__(self, error_code, error_category, error_owner, description):
        """

        :param error_code: The error code
        :param error_category: the error category
        :param error_owner: The identifier (code) of the error owner
        :param description: A text description of the error
        """
        self.error_code = error_code
        self.error_category = error_category
        self.error_owner = error_owner
        self.description = description

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "error_category": self.error_category,
            "error_owner": self.error_owner,
            "description": self.description,
        }

    def __str__(self):
        return str(self.to_dict())
