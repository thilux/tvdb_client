# coding: utf-8
from shared import BaseClient

__author__ = 'tsantana'


class ApiV1Client(BaseClient):

    def __init__(self, api_key):
        self.api_key = api_key

    def login(self):
        pass
