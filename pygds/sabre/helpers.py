import json
import xmltodict


def soap_service_to_json(data):
    """Transform a sabre soap api response to json format"""

    to_return_dict = None

    try:
        json_data = json.loads(json.dumps(xmltodict.parse(data.content)))

        if json_data is not None:
            to_return = json_data["soap-env:Envelope"]["soap-env:Body"]
            to_return = str(to_return).replace("@", "")
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
