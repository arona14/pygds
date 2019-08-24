# This file will be change for refactoring purpose.

from pygds.core.helpers import get_data_from_xml as from_xml


def get_data_from_json(data, main_tag):

    json_data = from_xml(data)
    if "soap-env:Envelope" not in json_data:
        return json_data
    to_return = json_data["soap-env:Envelope"]["soap-env:Body"][str(main_tag)]
    to_return = str(to_return).replace("@", "")
    to_return = eval(str(to_return).replace("u'", "'"))

    return to_return
