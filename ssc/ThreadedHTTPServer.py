from http.server import HTTPServer
import logging
import socket
from socketserver import TCPServer, ThreadingMixIn

from ssc.HTTPRequestHandler import HTTPRequestHandler
from ssc.ServletContainer import ServletContainer


logger = logging.getLogger(__name__)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, rootDir, port, tempDir):
        self._servletContainer = ServletContainer(self, rootDir, tempDir)

        TCPServer.__init__(self, ("", 13099), HTTPRequestHandler)

    @property
    def servletContainer(self):
        return self._servletContainer

    def server_bind(self):
        self.allow_reuse_address = True
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def serve_forever(self):
        while self._running:
            self.handle_request()

    def start(self):
        logger.debug('Server running')

        self._running = True

        self.serve_forever()

