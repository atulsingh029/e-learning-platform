"""
author   : github.com/atulsingh029
added in : version 2.0.0
"""

from .data_structure_classes import *
from custom_user.models import Account
from .object_provider import CacheUser
# this file contains business logic for memcache


class Authorization:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cacheStore = UserList()

    def get_authorization_data(self, username):
        result = self.cacheStore.search(username)
        if result is False:
            obj = Account.objects.get(username=username)
            user = CacheUser(obj)
            self.cacheStore.add(user)
            return user
        else:
            return result
