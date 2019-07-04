from lxml import etree


def parse_xml(xml_content: str):
    """
        Parses XML from String representation
    """
    return etree.fromstring(xml_content)


def extract_list_elements(tree_data, *x_path_expressions):
    """
        Extract elements as list from a tree data (parsed with #parse_xml):
        :Param tree_data: is the data parsed from method #parse_xml
    """
    return (tree_data.xpath(x) for x in x_path_expressions)


def extract_single_elements(tree_data, *x_path_expressions):
    """
    """
    return (tree_data.xpath(x)[0] for x in x_path_expressions)
