import logging
import os

from ssc.http.HTTP import MIME_CSS, MIME_TEXT, MIME_IMAGE_JPEG, MIME_IMAGE_PNG, \
    MIME_JSON, CODE_OK, HDR_CONTENT_TYPE, HDR_CONTENT_LENGTH, MIME_BINARY, \
    MIME_SVG, CODE_NOT_FOUND


logger = logging.getLogger(__name__)

class FileServlet:
    CHUNK_SIZE = 1024

    CONTENT_TYPE_MAP = {
         ('.css',) : MIME_CSS,
         ('.txt', '.py', '.c', '.cpp', '.h', '.java', '.js', '.html') : MIME_TEXT,
         ('.jpg', '.jpeg') : MIME_IMAGE_JPEG,
         ('.png',) : MIME_IMAGE_PNG,
         ('.json',) : MIME_JSON,
         ('.svg',) : MIME_SVG

    }

    def __init__(self, servletContainer):
        self._container = servletContainer

    def downloadFile(self, relPath, response):
        filePath = os.path.join(self._container.rootDir, relPath)

        if not os.path.isfile(filePath):
            logger.error('File not found %r' % filePath)
            response.sendResponse(CODE_NOT_FOUND)

            response.write('<html><body>File not found</body></html>')

            return True

        with open(filePath, 'rb') as fileObj:
            statInfo = os.stat(filePath)

            response.sendResponse(CODE_OK)
            response.sendHeader(HDR_CONTENT_TYPE, self._guessContentType(filePath))
            response.sendHeader(HDR_CONTENT_LENGTH, str(statInfo.st_size))

            while True:
                chunk = fileObj.read(self.CHUNK_SIZE)
                response.write(chunk)

                if len(chunk) < self.CHUNK_SIZE:
                    return True

    def handleRequest(self, request, response):
        return self.downloadFile(request.url.path[1:], response)

    def _guessContentType(self, path):
        ext = os.path.splitext(path)[1]

        for i in self.CONTENT_TYPE_MAP:
            if ext in i:
                return self.CONTENT_TYPE_MAP[i]

        return MIME_BINARY
