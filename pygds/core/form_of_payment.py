from typing import Dict
import json


class FormOfPaymentBasic:
    def to_data(self):
        """
            Method that returns a dictionary containing useful data. Must be implemented by sub-classes
        """
        raise NotImplementedError(" this is not yet implemented")

    def to_json(self):
        """
            Dumps the object to json string
        """
        return json.dumps(self.to_data(), indent=4)

    def __repr__(self):
        """
            method that redefined the string type
        """
        return self.to_json()


class FormOfPayment(FormOfPaymentBasic):

    def __init__(self, fop_reference: Dict, mop_description: Dict):
        self.fop_reference = fop_reference
        self.mop_description = mop_description

    def to_data(self):
        return {
            "fop_reference": self.fop_reference,
            "mop_description": self.mop_description
        }
