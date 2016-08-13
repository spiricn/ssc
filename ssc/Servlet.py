import os
import re

from mako.lookup import TemplateLookup
from mako.runtime import Context
from mako.template import Template as MakoTemplate

from ssc.FileWatcher import FileWatcher


class Servlet:
    def __init__(self, servletContainer, manifestEntry, sourceChangeCallback):
        self._servletContainer = servletContainer

        fullServletPath = os.path.abspath(os.path.join(servletContainer.rootDir, manifestEntry.file))

        templateLookup = TemplateLookup(directories=['/'],
                       module_directory=self.servletContainer.rootDir
        )

        self._makoTemplate = MakoTemplate(filename=fullServletPath, lookup=templateLookup)

        self._regex = [re.compile(i) for i in manifestEntry.pattern]

        self._manifestEntry = manifestEntry

        self._sourceChangeCallback = sourceChangeCallback

        self._fileWatcher = FileWatcher(fullServletPath, lambda path: self._sourceChangeCallback(self))

        self._fileWatcher.start()

    def unload(self):
        self._fileWatcher.stop()

    @property
    def manifestEntry(self):
        return self._manifestEntry

    @property
    def regex(self):
        return self._regex

    @property
    def servletContainer(self):
        return self._servletContainer

    def handleRequest(self, request, response):
        response.sendResponse(200)

        response.sendHeader('Content-type', 'text/html')

        self._makoTemplate.render_context(Context(response, request=request, response=response))

        return True
