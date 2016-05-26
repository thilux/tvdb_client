tvdb_client: A python client library for the new TVDB API
=========================================================

The tvdb_client provides integration with the TheTVDB API and allows interaction with all of its public APIs in both
versions: V1 and V2.

The tvdb_client library will provide different client classes for the V1 and V2 API versions from TheTVDB for they are
very different conceptually and technically (V1 is HTTP Get request based with XML response, while V2 is all RESTful JSON
based).

This library is powered by the fantastic `python Requests library <https://github.com/kennethreitz/requests>`_ and the
awesome `python lxml <https://github.com/lxml/lxml>`_.

**tvdb_client is not supported nor endorsed by TheTVDB.**

Client Classes
--------------

- **ApiV1Client:** Provides access to TheTVDB V1 APIs which are based on HTTP Get requests with XML based responses. The API documentation from TheTVDB can be found `HERE <http://www.thetvdb.com/wiki/index.php/Programmers_API#Dynamic_Interfaces>`_.
- **ApiV2Client:** Provides access to TheTVDB V2 APIs which are all RESTfull JSON APIs. The API information is very well documented `HERE <https://api.thetvdb.com/swagger>`_.

V1 API Client
`````````````
The V1 API Client is implemented by class ApiV1Client. Its constructor takes the api key, as required by TheTVDB.

Currently, the implementation of the methods for its APIs is under development.


V2 API Client
`````````````

The V2 API Client is implemented on class ApiV2Client. Its constructor receives the user identification (api key,
username and account identified) as required by TheTVDB and optionally the language option.

This client implements method for all the APIs documented in `TheTVDB swagger <https://api.thetvdb.com/swagger>`_ with
the exception of those that returns information on the parameters required for certain APIs.

The client is very easy to use as provided by the example below:

.. code-block:: python

    >>> from tvdb_client import ApiV2Client
    >>> api_client = ApiV2Client('USERNAME', 'API_KEY', 'ACCOUNT_IDENTIFIER')
    >>> api_client.login()
    >>> api_client.is_authenticated
    True
    >>> series = api_client.search_series(name='Game of Thrones')
    >>> print series
    {u'data': [{u'status': u'Continuing', u'network': u'HBO', u'overview': u"Seven noble families fight for control of
    the mythical land of Westeros. Friction between the houses leads to full-scale war. All while a very ancient evil
    awakens in the farthest north. Amidst the war, a neglected military order of misfits, the Night's Watch, is all that
     stands between the realms of men and the icy horrors beyond.", u'seriesName': u'Game of Thrones', u'firstAired':
     u'2011-04-17', u'banner': u'graphical/121361-g19.jpg', u'id': 121361, u'aliases': []}, {u'status': u'Continuing',
     u'network': u'YouTube', u'overview': u'A spoof/parody Based on HBO\'s hit series "A Game of Thrones" and George RR
     Martin\'s A Song of Ice and Fire', u'seriesName': u'Game of Thrones: Cartoon Parody', u'firstAired': u'2011-05-07',
      u'banner': u'', u'id': 311939, u'aliases': []}]}
    >>> type(series)
    <type 'dict'>


Status and updates
==================

 * May 2016: Development started and API V2 Client is up for business!


Contact
=======

Should you have any questions, suggestions or wishes to contribute, please drop me an email at thilux.systems@gmail.com.







