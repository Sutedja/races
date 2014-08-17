__author__ = 'sutedja'

import re

def get_text_if_exists(soup_part, tag, attr_dict={}):
    element = soup_part.find(tag, attr_dict)
    return element.get_text().strip().encode('utf-8') if element else ''

def clean_string(text, utf8=False):
    p = re.compile("|".join(["\xc2\xa0", "\n"]))
    if not utf8:
        text = text.encode("utf-8")
    return p.sub(" ", text).replace("  ", " ")

