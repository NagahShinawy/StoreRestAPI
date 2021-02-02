def body_values_to_lower(body):
    return dict((parameter, value.lower()) for parameter, value in body.items())
