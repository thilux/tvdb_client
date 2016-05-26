from unittest import TestCase
from tvdb_client.clients import ApiV1Client, ApiV2Client
from tvdb_client.exceptions import UserNotLoggedInException

__author__ = 'tsantana'


class LoginTestCase(TestCase):

    def runTest(self):
        pass

    def test_001_01_api_v1_login_success(self):
        pass

    def test_001_02_api_v2_login_success(self):

        api = ApiV2Client('thilux', '463B5371A1FCB382', 'F40C8DCCA265D3F3')
        api.login()

        self.assertTrue(api.is_authenticated)

    def test_002_01_api_v1_login_invalid_api_key(self):
        pass

    def test_002_02_api_v2_login_invalid_api_key(self):
        api = ApiV2Client('thilux', 'XXXXXXXXXXX', 'F40C8DCCA265D3F3')
        api.login()

        self.assertFalse(api.is_authenticated)

    def test_003_01_api_v1_login_invalid_account_identifier(self):
        pass

    def test_003_02_api_v2_login_invalid_account_identifier(self):
        api = ApiV2Client('thilux', '463B5371A1FCB382', 'XXIHWDIHWIHIE')
        api.login()

        self.assertFalse(api.is_authenticated)

    def test_004_01_api_v1_login_invalid_username(self):
        pass

    def test_004_02_api_v2_login_invalid_username(self):
        api = ApiV2Client('shambalalalallala', '463B5371A1FCB382', 'F40C8DCCA265D3F3')
        api.login()

        self.assertFalse(api.is_authenticated)


class SearchTestCase(TestCase):

    def runTest(self):
        pass

    def test_001_01_api_v1_search_series_single_letter(self):

        pass

    def test_001_02_api_v2_search_series_single_letter(self):

        api = ApiV2Client('thilux', '463B5371A1FCB382', 'F40C8DCCA265D3F3')
        api.login()

        resp = api.search_series(name='a')

        self.assertIsNotNone(resp)
        self.assertIn('data', resp)
        self.assertGreater(len(resp['data']), 0)

    def test_002_01_api_v1_search_series_single_show(self):
        pass

    def test_002_02_api_v2_search_series_single_show(self):
        api = ApiV2Client('thilux', '463B5371A1FCB382', 'F40C8DCCA265D3F3', 'en')
        api.login()

        resp = api.search_series(name='Fear the walking dead')

        self.assertIsNotNone(resp)
        self.assertIn('data', resp)
        self.assertEqual(len(resp['data']), 1)

    def test_003_01_api_v1_search_series_nonexistent(self):
        pass

    def test_003_02_api_v1_search_series_nonexistent(self):
        api = ApiV2Client('thilux', '463B5371A1FCB382', 'F40C8DCCA265D3F3', 'en')
        api.login()

        resp = api.search_series(name='Dosh Dosh Stoy Stoy Stoy')

        self.assertIsNotNone(resp)
        self.assertNotIn('data', resp)
        self.assertEqual(api.__class__.__name__, resp['client_class'])
        self.assertEqual(404, resp['code'])

    def test_004_01_api_v1_search_series_not_logged_in(self):
        pass

    def test_004_02_api_v2_search_series_not_logged_id(self):
        api = ApiV2Client('thilux', '463B5371A1FCB382', 'F40C8DCCA265D3F3', 'en')

        self.assertRaises(UserNotLoggedInException, callableObj=api.search_series, name='Fear the walking dead')


