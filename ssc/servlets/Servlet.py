import re

from ssc.http.HTTP import CODE_NOT_IMPLEMENTED


class Servlet:
    def __init__(self, servletContainer, pattern):
        self._servletContainer = servletContainer

        self._regex = re.compile(pattern) if pattern else None

    @property
    def regex(self):
        return self._regex

    def unload(self):
        pass

    @property
    def servletContainer(self):
        return self._servletContainer

    def handleRequest(self, request, response):
        response.sendResponse(CODE_NOT_IMPLEMENTED)

        return True
