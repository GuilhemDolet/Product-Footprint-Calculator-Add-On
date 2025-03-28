import re

url = "/waterheaters/Label_2307289.svg"


def regex_for_id(url):

    pattern = r'Label_\d{7}'
    match = re.search(pattern, url)

    if match:
        return match.group()
    else:
        return None


print(regex_for_id(url))