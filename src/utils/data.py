import re


def body_values_to_lower(body: dict):
    body_to_lower = dict()
    for parameter, value in body.items():
        if parameter == "country":
            body_to_lower.update({parameter: value})
        else:
            body_to_lower.update({parameter: value.lower()})
    return body_to_lower


def sort_list_of_dict(data, key_name):
    return sorted(data, key=lambda item: item[key_name])


def image_extension_url(image_url):
    regex_image_url = re.compile(r'(http)?s?:?(\/\/[^"\']*\.(?:png|jpg|jpeg))')
