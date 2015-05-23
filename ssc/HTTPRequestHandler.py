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
