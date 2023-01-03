import re
import logging
import traceback

modul_Logger = logging.getLogger('imdb_quest.scraper.helper.functions')


def get_search_safely(response, xpath: str, default_return: str) -> str:
    """
    Get the xpath value from response object. If the xpath not valid send back the default value.

    :param response:
    :param xpath:
    :param default_return:
    :return:
    """
    try:
        return response.xpath(xpath).get()
    except Exception as err:
        modul_Logger.error(err)
        traceback.print_exc()
        return default_return


def get_number_of_oscars(raw_str: str) -> str:
    """
    Get the number of Oscar awards from the string.

    :param raw_str:  String containing the highest awards from a movie.
    :return: String contains the number of oscars if there is any.
    """
    try:
        found = re.search(r"Won [\d]+ Oscar", raw_str)
        return found.group(0).replace("Won ", "").replace(" Oscar", "")
    except Exception:
        return "0"


def value_converter(x: str) -> str:
    """
    Convert string with number like K, M, B to numbers.

    :param x: String that contains a number.
    :return: The string converted to integer.
    """
    if 'K' in x:
        if len(x) > 1:
            return str(int(float(x.replace('K', '')) * 1000))
        return str(1000)
    if 'M' in x:
        if len(x) > 1:
            return str(int(float(x.replace('M', '')) * 1000000))
        return str(1000000)
    if 'B' in x:
        return str(int(float(x.replace('B', '')) * 1000000000))
    return str(0)
