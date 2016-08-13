import os


class FileServlet:
    CHUNK_SIZE = 1024

    def __init__(self, servletContainer):
        self._container = servletContainer

    def handleRequest(self, request, response):
        filePath = os.path.join(self._container.rootDir, request.url.path[1:])

        with open(filePath, 'rb') as fileObj:
            response.sendResponse(200)
            response.sendHeader('Content-type', 'application/octet-stream')

            while True:
                chunk = fileObj.read(self.CHUNK_SIZE)
                response.write(chunk)

                if len(chunk) < self.CHUNK_SIZE:
                    return True
