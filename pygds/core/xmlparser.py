# coding: utf-8
__author__ = "Mouhamad Ndiankho THIAM"
__copyright__ = "Copyright 2019, CTS"
__credits__ = ["Mouhamad Ndiankho THIAM", "Demba FALL", "Saliou Ndiouck"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Mouhamad Ndiankho THIAM"
__email__ = "mohamed@ctsfares.com"
__status__ = "Development"

"""
This module is for parsing and extracting data from XML
"""

from lxml import etree


def parse_xml(xml_content: str):
    """
        Parses XML from String representation
        :param xml_content: The string containing XML
        :return: Returns an XML Element
    """
    return etree.fromstring(xml_content)


def extract_list_elements(tree_data, *x_path_expressions):
    """
        Extract elements as list elements from a tree data (parsed with #parse_xml):
        :param tree_data: is the data parsed from method #parse_xml
        :param *x_path_expressions: is a list of XPATH expressions
        :return: Returns a tuple containing list elements corresponding to XPATH expressions
    """
    return (tree_data.xpath(x) for x in x_path_expressions)


def extract_single_elements(tree_data, *x_path_expressions):
    """
        Extract elements as signle elements from a tree data (parsed with #parse_xml):
        :param tree_data: is the data parsed from method #parse_xml
        :param *x_path_expressions: is a list of XPATH expressions
        :return: Returns a tuple containing single elements corresponding to XPATH expressions retrieved
    """
    # return (elms[0] if len(elms) > 0 else None for elms in tree_data.xpath(x) for x in x_path_expressions)
    return (x[0] if len(x) > 0 else None for x in extract_list_elements(tree_data, *x_path_expressions))
