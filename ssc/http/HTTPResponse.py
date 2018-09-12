from ssc.http.HTTP import HDR_CONNECTION, CONNECTION_CLOSE


class HTTPResponse:

    def __init__(self, handler):
        self._handler = handler

        self._responseSent = False
        self._headersSent = False
        self._headers = {}

    def addHeader(self, key, value):
        if self._headersSent:
            raise RuntimeError('Attempting to send header after sending data')

        self._headers[key] = value

    def sendResponse(self, code):
        if self._responseSent:
            raise RuntimeError('Attempting to send multiple responses')

        self._handler.send_response(code)

        self._responseSent = True

        self.sendHeader(HDR_CONNECTION, CONNECTION_CLOSE)

        for key, value in self._headers.items():
            self.sendHeader(key, value)

    def flush(self):
        self._handler.wfile.flush()

    def sendHeader(self, key, value):
        if not self._responseSent:
            raise RuntimeError('Must first send response before sending headers')

        if self._headersSent:
            raise RuntimeError('Attempting to send header after sending data')

        self._handler.send_header(key, value)

    def finish(self):
        if not self._responseSent:
            raise RuntimeError('Must first send response before finishing')

        if not self._headersSent:
            self._handler.end_headers()
            self._headersSent = True

    def write(self, data):
        if not self._responseSent:
            raise RuntimeError('Must first send response before sending data')

        if not self._headersSent:
            self._handler.end_headers()

            self._headersSent = True

        if isinstance(data, bytes):
            try:
                self._handler.wfile.write(data)
            except ConnectionAbortedError:
                return False
        else:
            self._handler.wfile.write(bytes(data.encode('utf-8')))
            return True

    def __iadd__(self, data):
        self.write(data)

        return self
