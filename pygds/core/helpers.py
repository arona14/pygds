import xmltodict
import json


def get_data_from_json(json_data, *paths):
    """
        This function retrieves data from json data by reading throught the list of paths given to it.
    """
    value = json_data
    for path in paths:
        if value is None:
            return None
        value = value[path]
    return value


def get_data_from_xml(xml_data, *paths):
    """
        Same as get_data_from_json but works on XML
    """
    json_data = json.loads(json.dumps(xmltodict.parse(xml_data)))
    return get_data_from_json(json_data, *paths)


def ensure_list(elem):
    """
        This function ensures that a given parameter is a list by creating a list of signe element if it is not.
    """
    return elem if isinstance(elem, list) else [elem]
