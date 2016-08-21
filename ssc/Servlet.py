import re


class Servlet:
    def __init__(self, servletContainer, pattern):
        self._servletContainer = servletContainer

        self._regex = re.compile(pattern) if pattern else None

    @property
    def regex(self):
        return self._regex

    @property
    def servletContainer(self):
        return self._servletContainer

    def handleRequest(self, request, response):
        response.sendResponse(404)

        return True
