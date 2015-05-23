class HTTPResponse:
    def __init__(self, handler):
        self._handler = handler

        self._responseSent = False

        self._headersSent = False

    def sendResponse(self, code):
        if self._responseSent:
            raise RuntimeError('Attempting to send multiple responses')

        self._handler.send_response(code)

        self._responseSent = True

    def sendHeader(self, key, value):
        if not self._responseSent:
            raise RuntimeError('Must first send response before sending headers')

        if self._headersSent:
            raise RuntimeError('Attempting to send header after sending data')

        self._handler.send_header(key, value)

    def write(self, data):
        if not self._responseSent:
            raise RuntimeError('Must first send response before sending data')

        if not self._headersSent:
            self._handler.end_headers()

            self._headersSent = True

        self._handler.wfile.write(bytes(data.encode('utf-8')))
