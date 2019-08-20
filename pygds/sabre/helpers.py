# This file will be change for refactoring purpose.

import json
import xmltodict
from time import gmtime, strftime

def soap_service_to_json(data):
    """Transform a sabre soap api response content to json format
    PS: This transformation is specific to SABRE
    """

    to_return_dict = None

    try:
        json_data = json.loads(json.dumps(xmltodict.parse(data)))

        if json_data:
            if 'soapenv:Envelope' in json_data:
                to_return = json_data["soapenv:Envelope"]["soapenv:Body"]
            else:
                to_return = json_data["soap-env:Envelope"]["soap-env:Body"]
            to_return = str(to_return).replace("@", "")
            to_return = str(to_return).replace("stl19:", "")
            to_return = str(to_return).replace("or114:", "")
            to_return_dict = eval(to_return.replace("u'", "'"))

            del to_return_dict["xmlns:stl19"]
            del to_return_dict["xmlns:ns6"]
            del to_return_dict["xmlns:or114"]
            del to_return_dict["xmlns:raw"]
            del to_return_dict["xmlns:ns4"]
        return to_return_dict
    except:
        # TODO: Capture the real exception not the general one
        pass
    return to_return_dict

def get_current_timestamp():
    current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S",gmtime()))
    return current_timestamp


def main():
    pass


if __name__ == "__main__":
    main()
