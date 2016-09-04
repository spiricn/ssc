import logging
import os

from ssc.http.HTTP import EXT_TO_CONTENT_TYPE, MIME_BINARY, CODE_OK, \
    HDR_CONTENT_TYPE, HDR_CONTENT_LENGTH


logger = logging.getLogger(__name__)

class FileServlet:
    CHUNK_SIZE = 1024

    def __init__(self, servletContainer):
        self._container = servletContainer

    def handleRequest(self, request, response):
        return self.downloadFile(request.url.path[1:], response)

    def _guessContentType(self, path):
        ext = os.path.splitext(path)[1]

        for i in EXT_TO_CONTENT_TYPE:
            if ext in i:
                return EXT_TO_CONTENT_TYPE[i]

        logger.warning('unrecognized file extension: %r' % ext)

        return MIME_BINARY

    def downloadFile(self, relPath, response):
        filePath = os.path.join(self._container.rootDir, relPath)

        if not os.path.isfile(filePath):
            logger.error('File not found %r' % filePath)
            return False

        try:
            fileObj = open(filePath, 'rb')
        except Exception as e:
            logger.error('Error opening file %r for reading: %s' % (filePath, str(e)))
            return False

        statInfo = os.stat(filePath)

        response.sendResponse(CODE_OK)
        response.sendHeader(HDR_CONTENT_TYPE, self._guessContentType(filePath))
        response.sendHeader(HDR_CONTENT_LENGTH, str(statInfo.st_size))

        while True:
            chunk = fileObj.read(self.CHUNK_SIZE)
            response.write(chunk)

            if len(chunk) < self.CHUNK_SIZE:
                break

        fileObj.close()

        return True
