from collections import namedtuple, OrderedDict
import json
import logging


from ssc.http.HTTP import HDR_CONTENT_TYPE, CODE_BAD_REQUEST, MIME_HTML, CODE_OK, \
    MIME_JSON, HDR_TRANSFER_ENCODING, TRANSFER_ENCODING_CHUNKED
from ssc.servlets.Servlet import Servlet


logger = logging.getLogger(__name__)

RestHandler = namedtuple('RestHandler', 'path, callback, help, chunked')
RestHandler.__new__.__defaults__ = (None,) * len(RestHandler._fields)

class RestServlet(Servlet):
    def __init__(self, servletContainer, pattern):
        Servlet.__init__(self, servletContainer, pattern)

        self._handlers = []

        self.addHandler(RestHandler('api', self._apiDisplay))

    @property
    def handlers(self):
        return self._handlers

    def addApi(self, api):
        for handler in api:
            self.addHandler(handler)

    def addHandler(self, handler):
        self._handlers.append(handler)

    @classmethod
    def objToJson(cls, obj):
        if isinstance(obj, tuple):
            return cls.objToJson(obj._asdict())
        elif isinstance(obj, OrderedDict):
            return cls.objToJson(dict(obj))
        elif obj == None:
            return ''
        elif hasattr(obj, '_asdict'):
            return cls.objToJson(obj._asdict())
        elif isinstance(obj, dict):
            return json.dumps(obj)
        else:
            return str(obj)

    def sendChunk(self, response, data):
        chunkLength = hex(len(data))[2:] if data else '0'

        response.write(chunkLength)
        response.write('\r\n')
        if data:
            response.write(data)
        response.write('\r\n')
        response.flush()

    def handleRequest(self, request, response):
        path = request.url.path.split('/')[2:]

        path = '/'.join(path)

        for handler in self._handlers:
            if handler.path == path:
                code, mime, res = handler.callback(request)
                response.sendResponse(code)
                response.sendHeader(HDR_CONTENT_TYPE, mime)

                if not handler.chunked:
                    response.write(self.objToJson(res))

                    return True

                else:
                    response.sendHeader(HDR_TRANSFER_ENCODING, TRANSFER_ENCODING_CHUNKED)

                    for data in res:
                        self.sendChunk(response, data)

                    self.sendChunk(response, None)

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

