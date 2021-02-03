def body_values_to_lower(body: dict):
    body_to_lower = dict()
    for parameter, value in body.items():
        if parameter == "country":
            body_to_lower.update({parameter: value})
        else:
            body_to_lower.update({parameter: value.lower()})
    return body_to_lower
