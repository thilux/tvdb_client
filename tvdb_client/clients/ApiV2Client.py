# coding: utf-8
from shared import BaseClient, authentication_required
from datetime import datetime, timedelta
from tvdb_client.utils import requests_util, utils
from tvdb_client.exceptions import AuthenticationFailedException
import json

__author__ = 'tsantana'


class ApiV2Client(BaseClient):
    """
    This is the python library implementation of the TheTVDB API V2. Details of the APIs is documented in the swagger
    page maintained by TheTVDB that can be found on this address: https://api.thetvdb.com/swagger

    The only APIs not represented by methods in this library are the ones that only returns parameters information of
    the actual API.
    """

    API_BASE_URL = 'https://api.thetvdb.com'
    TOKEN_DURATION_SECONDS = 23 * 3600  # 23 Hours
    TOKEN_MAX_DURATION = 24 * 3600  # 24 Hours

    def __init__(self, username, api_key, account_identifier, language=None):
        self.username = username
        self.api_key = api_key
        self.account_identifier = account_identifier
        self.is_authenticated = False
        self.__token = None
        self.__auth_time = 0
        self.language = language

    def __get_header(self):
        header = dict()
        header['Content-Type'] = 'application/json'

        if self.language:
            header['Accept-Language'] = self.language

        return header

    def __refresh_token(self):
        headers = self.__get_header()
        headers['Authorization'] = 'Bearer %s' % self.__token

        resp = requests_util.run_request('get', self.API_BASE_URL + '/refresh_token', headers=headers)

        if resp.status_code == 200:
            token_resp = json.loads(resp.content)
            self.__token = token_resp['token']
            self.__auth_time = datetime.now()

    def __get_header_with_auth(self):
        """
        This private method returns the HTTP heder filled with the Authorization information with the user token.
        The token validity is monitored whenever this function is called, so according to the swagger page of TheTVDB
        (https://api.thetvdb.com/swagger) the tokens are valid for 24 hours, therefore if a token is generated for over
        23 hours already, this function will also perform a token refresh using TheTVDB refresh_token API. If over 24
        hours have passed since the token generation, a login is performed to generate a new one, instead.

        :return: A python dictionary representing the HTTP header to be used in TheTVDB API calls.
        """
        auth_header = self.__get_header()
        auth_header['Authorization'] = 'Bearer %s' % self.__token
        token_renew_time = self.__auth_time + timedelta(seconds=self.TOKEN_DURATION_SECONDS)

        if datetime.now() > token_renew_time:
            token_max_time = self.__auth_time + timedelta(seconds=self.TOKEN_MAX_DURATION)
            if datetime.now() < token_max_time:
                self.__refresh_token()
            else:
                self.login()

            auth_header['Authorization'] = 'Bearer %s' % self.__token

        return auth_header

    def login(self):
        """
        This method performs the login on TheTVDB given the api key, user name and account identifier.

        :return: None
        """
        auth_data = dict()
        auth_data['apikey'] = self.api_key
        auth_data['username'] = self.username
        auth_data['userkey'] = self.account_identifier

        auth_resp = requests_util.run_request('post', self.API_BASE_URL + '/login', data=json.dumps(auth_data),
                                              headers=self.__get_header())

        if auth_resp.status_code == 200:
            auth_resp_data = json.loads(auth_resp.content)
            self.__token = auth_resp_data['token']
            self.__auth_time = datetime.now()
            self.is_authenticated = True
        else:
            raise AuthenticationFailedException('Authentication failed!')

    @authentication_required
    def search_series(self, name=None, imdb_id=None, zap2it_id=None):
        """
        Searchs for a series in TheTVDB by either its name, imdb_id or zap2it_id.

        :param name: the name of the series to look for
        :param imdb_id: the IMDB id of the series to look for
        :param zap2it_id: the zap2it id of the series to look for.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """
        arguments = locals()
        optional_parameters = {'name': 'name', 'imdb_id': 'imdbId', 'zap2it_id': 'zap2itId'}

        query_string = utils.query_param_string_from_option_args(optional_parameters, arguments)

        raw_response = requests_util.run_request('get', '%s%s?%s' % (self.API_BASE_URL, '/search/series',
                                                                     query_string),
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series(self, series_id):
        """
        Retrieves the information of a series from TheTVDB given the series ID.

        :param series_id: the id of the series on TheTVDB.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d' % series_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series_actors(self, series_id):
        """
        Retrieves the information on the actors of a particular series, given its TheTVDB id.

        :param series_id: the TheTVDB id of the series
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/actors' % series_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series_episodes(self, series_id, page=1):
        """
        Retrieves all episodes for a particular series given its TheTVDB id. It retrieves a maximum of 100 results per
        page.

        :param series_id: The TheTVDB id of the series.
        :param page: The page number. If none is provided, 1 is used by default.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/episodes?page=%d' %
                                                 (series_id, page), headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series_episodes(self, series_id, episode_number=None, aired_season=None, aired_episode=None,
                            dvd_season=None, dvd_episode=None, imdb_id=None, page=1):

        """
        Retrieves all episodes for a particular series given its TheTVDB and filtered by additional optional details.

        :param series_id: The TheTVDB id of the series.
        :param episode_number: The optional absolute episode number.
        :param aired_season: The optional aired season number.
        :param aired_episode: The optional aired episode number.
        :param dvd_season: The optional DVD season number.
        :param dvd_episode: The optional DVD episode number.
        :param imdb_id: The optional IMDB Id of the series.
        :param page: The page number. If none is provided, 1 is used by default.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        arguments = locals()
        optional_parameters = {'episode_number': 'absoluteNumber', 'aired_season': 'airedSeason',
                               'aired_episode': 'airedEpisode', 'dvd_season': 'dvdSeason', 'dvd_episode': 'dvdEpisode',
                               'imdb_id': 'imdbId', 'page': 'page'}

        query_string = utils.query_param_string_from_option_args(optional_parameters, arguments)

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/episodes/query?%s' %
                                                 (series_id, query_string), headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series_episodes_summary(self, series_id):
        """
        Retrieves the summary of the episodes and seasons of a series given its TheTVDB id.

        :param series_id: The TheTVDB id of the series.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/episodes/summary' % series_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def __get_series_images(self, series_id):
        """
        Retrieves the url to images (posters, fanart) for the series, seasons and episodes of a series given its
        TheTVDB id.

        :param series_id: The TheTVDB id of the series.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/images' % series_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_series_images(self, series_id, image_type=None, resolution=None, sub_key=None):
        """
        Retrieves the url to images (posters, fanart) for the series, seasons and episodes of a series given its
        TheTVDB id and filtered by additional parameters.

        :param series_id: The TheTVDB id of the series.
        :param image_type: The optional type of image: posters, fanart, thumbnail, etc.
        :param resolution: The optional resolution: i.e. 1280x1024
        :param sub_key: The optional subkey: graphical, text.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        arguments = locals()
        optional_parameters = {'image_type': 'keyType', 'resolution': 'resolution', 'sub_key': 'subKey'}

        query_string = utils.query_param_string_from_option_args(optional_parameters, arguments)

        if len(query_string):

            raw_response = requests_util.run_request('get', self.API_BASE_URL + '/series/%d/images/query?%s' %
                                                     (series_id, query_string), headers=self.__get_header_with_auth())
            return self.parse_raw_response(raw_response)
        else:
            return self.__get_series_images(series_id)

    @authentication_required
    def get_updated(self, from_time, to_time=None):
        """
        Retrives a list of series that have changed on TheTVDB since a provided from time parameter and optionally to an
        specified to time.

        :param from_time: An epoch representation of the date from which to restrict the query to.
        :param to_time: An optional epcoh representation of the date to which to restrict the query to.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        arguments = locals()
        optional_parameters = {'to_time': 'toTime'}

        query_string = 'fromTime=%s&%s' % (from_time,
                                           utils.query_param_string_from_option_args(optional_parameters, arguments))

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/uodated/query?%s' % query_string,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_user(self):
        """
        Retrieves information about the user currently using the api.

        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        return self.parse_raw_response(requests_util.run_request('get', self.API_BASE_URL + '/user',
                                                                 headers=self.__get_header_with_auth()))

    @authentication_required
    def get_user_favorites(self):
        """
        Retrieves the list of tv series the current user has flagged as favorite.

        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        return self.parse_raw_response(requests_util.run_request('get', self.API_BASE_URL + '/user/favorites',
                                                                 headers=self.__get_header_with_auth()))

    @authentication_required
    def delete_user_favorite(self, series_id):
        """
        Deletes the series of the provided id from the favorites list of the current user.

        :param series_id: The TheTVDB id of the series.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        return self.parse_raw_response(requests_util.run_request('delete',
                                                                 self.API_BASE_URL + '/user/favorites/%d' % series_id,
                                                                 headers=self.__get_header_with_auth()))

    @authentication_required
    def add_user_favorite(self, series_id):
        """
        Added the series related to the series id provided to the list of favorites of the current user.

        :param series_id: The TheTVDB id of the series.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        return self.parse_raw_response(requests_util.run_request('put',
                                                                 self.API_BASE_URL + '/user/favorites/%d' % series_id,
                                                                 headers=self.__get_header_with_auth()))

    @authentication_required
    def __get_user_ratings(self):
        """
        Returns a list of the ratings provided by the current user.

        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        return self.parse_raw_response(requests_util.run_request('get', self.API_BASE_URL + '/user/ratings',
                                                                 headers=self.__get_header_with_auth()))

    @authentication_required
    def get_user_ratings(self, item_type=None):
        """
        Returns a list of the ratings for the type of item provided, for the current user.

        :param item_type: One of: series, episode or banner.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        if item_type:
            query_string = 'itemType=%s' % item_type

            return self.parse_raw_response(
                requests_util.run_request('get', self.API_BASE_URL + '/user/ratings/qeury?%s' % query_string,
                                          headers=self.__get_header_with_auth()))
        else:
            return self.__get_user_ratings()

    @authentication_required
    def add_user_rating(self, item_type, item_id, item_rating):
        """
        Adds the rating for the item indicated for the current user.

        :param item_type: One of: series, episode, banner.
        :param item_id: The TheTVDB id of the item.
        :param item_rating: The rating from 0 to 10.
        :return:
        """

        raw_response = requests_util.run_request('put',
                                                 self.API_BASE_URL + '/user/ratings/%s/%d/%d' %
                                                 (item_type, item_id, item_rating),
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def delete_user_rating(self, item_type, item_id):
        """
        Deletes from the list of rating of the current user, the rating provided for the specified element type.

        :param item_type: One of: series, episode, banner.
        :param item_id: The TheTVDB Id of the item.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('delete',
                                                 self.API_BASE_URL + '/user/ratings/%s/%d' %
                                                 (item_type, item_id), headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_episode(self, episode_id):
        """
        Returns the full information of the episode belonging to the Id provided.

        :param episode_id: The TheTVDB id of the episode.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/episodes/%d' % episode_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_languages(self):
        """
        Returns a list of all language options available in TheTVDB.

        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/languages',
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)

    @authentication_required
    def get_language(self, language_id):
        """
        Retrieves information about the language of the given id.

        :param language_id: The TheTVDB Id of the language.
        :return: a python dictionary with either the result of the search or an error from TheTVDB.
        """

        raw_response = requests_util.run_request('get', self.API_BASE_URL + '/languages/%d' % language_id,
                                                 headers=self.__get_header_with_auth())

        return self.parse_raw_response(raw_response)
