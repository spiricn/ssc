import os


class FileServlet:
    CHUNK_SIZE = 1024

    CONTENT_TYPE_MAP = {
         ('.css',) : 'text/css',
         ('.txt', '.py', '.c', '.cpp', '.h', '.java', '.js', '.html') : 'text/plain',
         ('.jpg', '.jpeg') : 'image/jpeg',
         ('.png',) : 'image/png'

    }

    def __init__(self, servletContainer):
        self._container = servletContainer

    def handleRequest(self, request, response):
        filePath = os.path.join(self._container.rootDir, request.url.path[1:])

        with open(filePath, 'rb') as fileObj:
            statInfo = os.stat(filePath)

            response.sendResponse(200)
            response.sendHeader('Content-type', self._guessContentType(filePath))
            response.sendHeader('Content-length', str(statInfo.st_size))

            while True:
                chunk = fileObj.read(self.CHUNK_SIZE)
                response.write(chunk)

                if len(chunk) < self.CHUNK_SIZE:
                    return True

    def _guessContentType(self, path):
        ext = os.path.splitext(path)[1]

        for i in self.CONTENT_TYPE_MAP:
            if ext in i:
                print(ext, self.CONTENT_TYPE_MAP[i])
                return self.CONTENT_TYPE_MAP[i]

        return 'application/octet-stream'
