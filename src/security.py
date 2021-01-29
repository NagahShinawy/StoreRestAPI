from models.user import UserModel


# users = [User(1, "bob", "123456")]
#
# username_mapping = {user.username: user for user in users}
# userid_mapping = {user.id: user for user in users}


def authenticate(username, password):
    # user = username_mapping.get(username)
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user
    return False


def identity(payload):
    """
    :param payload: content of jwt token (decode the token to content)
    jwt calls identity function when it is used by POST, GET , ..... http methods
    :return: user based on user id
    """
    """
    {
          "exp": 1611301305,
          "iat": 1611301005,
          "nbf": 1611301005,
          "identity": 1
    }
    """
    # user = userid_mapping.get(payload["identity"], None)
    user_id = payload["identity"]
    user = UserModel.find_by_id(user_id)
    return user
