# coding: utf-8
from tvdb_client.exceptions import UserNotLoggedInException
import abc
import json


__author__ = 'tsantana'


def authentication_required(func):
        def inner(instance, *args, **kwargs):
            if not instance.is_authenticated:
                raise UserNotLoggedInException('Authentication is required!')
            else:
                return func(instance, *args, **kwargs)
        return inner


class BaseClient(object):

    @abc.abstractmethod
    def login(self):
        pass

    @abc.abstractmethod
    def search_series(self, name=None, imdb_id=None, zap2it_id=None):
        """
        Searchs for a series given its name, imdb_id or zap2it_id.
        :param name:
        :param imdb_id:
        :param zap2it_id:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_series(self, series_id):
        pass

    @abc.abstractmethod
    def get_series_episodes(self, series_id, page=1):
        pass

    @abc.abstractmethod
    def get_series_episodes(self, series_id, episode_number=None, aired_season=None, aired_episode=None,
                            dvd_season=None, dvd_episode=None, imdb_id=None, page=1):
        pass

    @abc.abstractmethod
    def get_series_images(self, series_id):
        pass

    @abc.abstractmethod
    def get_series_images(self, series_id, image_type=None, resolution=None, sub_key=None):
        pass

    @abc.abstractmethod
    def get_series_episodes_summary(self, series_id):
        pass

    @abc.abstractmethod
    def get_series_actors(self, series_id):
        pass

    @abc.abstractmethod
    def get_episode(self, episode_id):
        pass

    @abc.abstractmethod
    def get_languages(self):
        pass

    @abc.abstractmethod
    def get_language(self, language_id):
        pass

    @abc.abstractmethod
    def get_updated(self, from_time, to_time=None):
        pass

    @abc.abstractmethod
    def get_user(self):
        pass

    @abc.abstractmethod
    def get_user_favorites(self):
        pass

    @abc.abstractmethod
    def delete_user_favorite(self, series_id):
        pass

    @abc.abstractmethod
    def add_user_favorite(self, series_id):
        pass

    @abc.abstractmethod
    def __get_user_ratings(self):
        pass

    @abc.abstractmethod
    def get_user_ratings(self, item_type=None):
        pass

    @abc.abstractmethod
    def add_user_rating(self, item_type, item_id, item_rating):
        pass

    @abc.abstractmethod
    def delete_user_rating(self, item_type, item_id):
        pass

    def __handle_error(self, raw_response):

        status_code = raw_response.status_code

        print 'Raw_response=>', raw_response.status_code, ' : ', raw_response.content

        error = dict()
        error['client_class'] = self.__class__.__name__
        error['code'] = status_code
        error['message'] = json.loads(raw_response.content)['Error']

        return error

    def parse_raw_response(self, raw_response):

        if raw_response.status_code == 200:
            return json.loads(raw_response.content)
        else:
            return self.__handle_error(raw_response)
