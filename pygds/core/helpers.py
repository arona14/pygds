import xmltodict
import json


def get_data_from_json(json_data, *paths):
    """
        This function retrieves data from json data by reading throught the list of paths given to it.
    """
    for path in paths:
        print(f"path: {path}")
        if json_data is None:
            return None
        json_data = json_data[path]
    return json_data


def get_data_from_xml(xml_data, *paths):
    """
        Same as get_data_from_json but works on XML
    """
    json_data = json.loads(json.dumps(xmltodict.parse(xml_data)))
    return get_data_from_json(json_data, *paths)
