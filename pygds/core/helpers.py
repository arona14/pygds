import time

import xmltodict
import json


def fareTypePriceQuote(passenger_type):
    fare_type = ""
    passenger_pub_list = ["ADT","CNN","C11","C10","C09","C08","C07","C06","C05","C04","C03","C02","INF"]
    if str(passenger_type).startswith("J") or str(passenger_type) not in passenger_pub_list:
        fare_type = "NET"
    else:
        fare_type = "PUB"
    return fare_type


def ensureList(elem):
    return elem if isinstance(elem, list) else [elem]


def get_data_from_json(json_data, *paths):
    """
    This function retrieves data from json data by reading through the list of paths given to it.
    :param json_data: The json data
    :param paths: List of paths to search for
    :return: The retrieved value
    :raises ValueError
    """
    value = json_data
    for path in paths:
        if value is None:
            return None
        value = value[path]
    return value


def get_data_from_json_safe(json_data, *paths):
    """
    Like `get_data_from_json` but without raising `KeyError`
    :param json_data: The json data
    :param paths: List of paths to search for
    :return: The retrieved value or None if one path doesn't exist
    """
    try:
        return get_data_from_json(json_data, *paths)
    except KeyError:
        return None


def get_data_from_xml(xml_data, *paths):
    """
    Same as get_data_from_json but works on XML
    :param xml_data: The XML data
    :param paths: List of paths to search for
    :return: The retrieved value
    :raises ValueError
    """
    json_data = json.loads(json.dumps(xmltodict.parse(xml_data)))
    return get_data_from_json(json_data, *paths)


def ensure_list(elem):
    """
    This function ensures that a given parameter is a list by creating a list of single element if it is not.
    :param elem: The element (can be any type)
    :return: List
    """
    return elem if isinstance(elem, list) else [elem] if elem else []


def reformat_date(date_time, input_format: str, output_format: str):
    """
    A function to reformat dates and times
    :param date_time: The str representation of the input
    :param input_format: The current format of the date or time
    :param output_format: The desired format
    :return: str: the date time formatted in the desired format
    """
    return time.strftime(output_format, time.strptime(date_time, input_format))
