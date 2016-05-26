import requests
import warnings

from requests.exceptions import RequestException

REQUEST_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


def __request_get(url, data=None, headers=None):
    return requests.get(url, params=data, headers=headers)


def __request_post(url, data=None, headers=None):
    return requests.post(url, data=data, headers=headers)


def __request_put(url, data=None, headers=None):
    return requests.put(url, data=data, headers=headers)


def __request_delete(url, data=None, headers=None):
    return requests.delete(url, data=data, headers=headers)


def __request_factory(request_type):

    if request_type.upper() in REQUEST_METHODS:
        func_name = eval('__request_%s' % request_type.lower())
        return func_name
    else:
        return None


def run_request(request_type, url, retries=5, data=None, headers=None):
    func = __request_factory(request_type)

    for attempt in range(retries+1):
        try:
            response = func(url, data=data, headers=headers)
            return response
        except RequestException:
            warnings.warn('Got error on request for attemp %d - %s' %
                          (attempt, 'retry is possible' if attempt < retries else 'no retry'))
    return None
