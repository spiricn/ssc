from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import logging

import ssc
from ssc.HTTPRequest import HTTPRequest
from ssc.HTTPResponse import HTTPResponse


logger = logging.getLogger(__name__)


class HTTPRequestHandler(BaseHTTPRequestHandler):
    '''
    Simple proxy class that delegates GET requests to the servlet container
    '''

    def __init__(self, request, client_address, server):
        self._server = server

        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        return self.server.servletContainer.handleRequest(HTTPRequest(self), HTTPResponse(self))

    def version_string(self):
        return 'SSC ' + ssc.__version__

    def log_message(self, format, *args):
        pass

    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s',
                         self.requestline, str(code), str(size))

    def log_error(self, format, *args):
        self.log_message(format, *args)
