from src.countries import COUNTRIES


def validate_username(username):
    if len(username) < 3:
        raise ValueError("username must be at least 3 chars")
    return username


def validate_country(user_country):
    for country_obj in COUNTRIES:
        if user_country in country_obj:
            return country_obj