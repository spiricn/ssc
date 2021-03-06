from http.server import HTTPServer
import logging
import socket
from socketserver import TCPServer, ThreadingMixIn
from threading import Thread

from ssc.http.HTTPRequestHandler import HTTPRequestHandler


logger = logging.getLogger(__name__)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, port, requestHandler):
        self._requestHandler = requestHandler
        self._port = port
        self._running = True

        TCPServer.__init__(self, (address, port), HTTPRequestHandler)

    @property
    def requestHandler(self):
        return self._requestHandler

    def server_bind(self):
        self.allow_reuse_address = True
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

        logger.debug('Starting TCP server at %s' % str(self.server_address))


    def start(self):
        self._thread = Thread(target=self.serve_forever)
        self._thread.setName('ServerThread')
        self._thread.start()

    def stop(self):
        self.shutdown()
        self._thread.join()
