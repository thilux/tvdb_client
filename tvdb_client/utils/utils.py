# encoding=latin-1
__author__ = 'tsantana'

import urllib

def query_param_string_from_option_args(a2q_dict, args_dict):
    """
    From a dictionary of arguments to query string parameters, loops through ad arguments list and makes a query string.
    :param a2q_dict: a dictionary containing argument_name > query string parameter name.
    :param args_dict: a dictionary containing the argument_name > argument_value
    :return: a query string.
    """

    name_value_pairs = dict()
    for ak in a2q_dict.keys():
        value = args_dict[ak]
        if value != None:
            name_value_pairs[a2q_dict[ak]] = str(value)

    return urllib.urlencode(name_value_pairs)


def make_str_content(content):
    """
    In python3+ requests.Response.content returns bytes instead of ol'good str.
    :param content: requests.Response.content
    :return: str representation of the requests.Response.content data
    """
    if not isinstance(content, str):
        content = str(content.decode())
    return content
