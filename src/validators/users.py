def validate_username(username):
    if len(username) < 3:
        raise ValueError("username must be at least 3 chars")
    return username
