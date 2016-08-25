from urllib.parse import urlparse, parse_qs

class HTTPRequest:
    GET, \
    POST = range(2)

    def __init__(self, handler):
        self._handler = handler

        self._url = urlparse(handler.path)

        self._type = HTTPRequest.GET

        self._params = parse_qs(self._url.query)

    @property
    def headers(self):
        return self._handler.headers

    @property
    def params(self):
        return self._params

    @property
    def type(self):
        return self._type

    @property
    def url(self):
        return self._url

    def __str__(self):
        return '{url=%r type=%d params=%r}' % (self._url, self._type, str(self._params))
