"""
author   : github.com/atulsingh029
added in : version 2.0.0
"""
# this file contains all the data structure definitions


class UserList(set):
    def search(self, username):
        for i in self:
            if i.username == str(username):
                return i
        else:
            return False