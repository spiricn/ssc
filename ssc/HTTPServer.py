import socket
from socketserver import TCPServer

from ssc.HTTPRequestHandler import HTTPRequestHandler
from ssc.Logger import Logger
from ssc.ServletContainer import ServletContainer


class HTTPServer(TCPServer):
    def __init__(self, rootDir, port):
        self._servletContainer = ServletContainer(self, rootDir)

        TCPServer.__init__(self, ("", port), HTTPRequestHandler)

        self._log = Logger(self)

    @property
    def servletContainer(self):
        return self._servletContainer

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def start(self):
        self._log.d('Server running')

        self.serve_forever()
