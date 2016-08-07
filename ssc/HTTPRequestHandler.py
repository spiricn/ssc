from http.server import SimpleHTTPRequestHandler

from ssc.HTTPRequest import HTTPRequest
from ssc.HTTPResponse import HTTPResponse


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    '''
    Simple proxy class that delegates GET requests to the servlet container
    '''

    def __init__(self, request, client_address, server):
        self._server = server

        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        return self.server.servletContainer.handleRequest(HTTPRequest(self), HTTPResponse(self))

    def log_message(self, format, *args):
        pass

    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s',
                         self.requestline, str(code), str(size))

    def log_error(self, format, *args):
        self.log_message(format, *args)
