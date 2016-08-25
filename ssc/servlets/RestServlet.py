from collections import namedtuple, OrderedDict
import json
import logging

from ssc.http.HTTP import HDR_CONTENT_TYPE, CODE_BAD_REQUEST, MIME_HTML, CODE_OK, \
    MIME_JSON
from ssc.servlets.Servlet import Servlet


logger = logging.getLogger(__name__)

RestHandler = namedtuple('RestHandler', 'path, callback, help')

class RestServlet(Servlet):
    def __init__(self, servletContainer, pattern):
        Servlet.__init__(self, servletContainer, pattern)

        self._handlers = []

        self.addHandler('api', self._apiDisplay)

    @property
    def handlers(self):
        return self._handlers

    def addApi(self, api):
        for path, callback in api:
            self.addHandler(path, callback)

    def addHandler(self, path, callback, helpDoc='N/A'):
        self._handlers.append(RestHandler(path, callback, helpDoc))

    def _parseType(self, obj):
        if isinstance(obj, tuple):
            return self._parseType(obj._asdict())
        elif isinstance(obj, OrderedDict):
            return self._parseType(dict(obj))
        elif isinstance(obj, dict):
            return json.dumps(obj)
        elif obj == None:
            return ''
        else:
            return str(obj)

    def handleRequest(self, request, response):
        path = request.url.path.split('/')[2:]

        path = '/'.join(path)

        for handler in self._handlers:
            if handler.path == path:
                code, mime, res = handler.callback(**request.params)
                response.sendResponse(code)
                response.sendHeader(HDR_CONTENT_TYPE, mime)

                response.write(self._parseType(res))

                return True

        logger.error('REST path %r not supported' % path)

        response.sendResponse(CODE_BAD_REQUEST)
        response.sendHeader(HDR_CONTENT_TYPE, MIME_HTML)
        response.write('<html> <body> Bad request </body> </html>')

        return True

    def _apiDisplay(self):
        res = []

        for handler in self._handlers:
            res.append({
                        'path' : handler.path,
                        'help' : handler.help
                        }
       )

        return (CODE_OK, MIME_JSON, res)

