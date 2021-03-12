"""
author   : github.com/atulsingh029
added in : version 2.0.0
"""
from memcache_layer.performance_layer import Authorization

authorization = Authorization(cache_size=1000)


def request_authorizer(request):
    """
    Methods authorizes users(requests).
    :param request: Request object
    :return: Returns User Object if authentication is true else AnonymousUser
    """
    if request.user.is_authenticated:
        username = request.user
        result = authorization.get_authorization_data(username)
        return result
    else:
        return 'AnonymousUser'
