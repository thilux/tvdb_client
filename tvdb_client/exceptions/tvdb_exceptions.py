__author__ = 'tsantana'


class UserNotLoggedInException(Exception):

    def __init__(self, message):
        super(UserNotLoggedInException, self).__init__(message)


class AuthenticationFailedException(Exception):

    def __init__(self, message):
        super(AuthenticationFailedException, self).__init__(message)
