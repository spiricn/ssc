from mako.lookup import TemplateLookup
from mako.runtime import Context
from mako.template import Template as MakoTemplate
import os

from ssc.http.HTTP import CODE_OK, HDR_CONTENT_TYPE, MIME_HTML
from ssc.servlets.Servlet import Servlet
from ssc.utils.FileWatcher import FileWatcher


class PageServlet(Servlet):
    def __init__(self, servletContainer, manifestEntry, sourceChangeCallback):
        Servlet.__init__(self, servletContainer, None if not manifestEntry else manifestEntry.pattern)
        self._servletContainer = servletContainer

        fullServletPath = os.path.abspath(os.path.join(servletContainer.rootDir, manifestEntry.filePath))

        templateLookup = TemplateLookup(directories=['/'],
                       module_directory=self.servletContainer.tempDir
        )

        self._makoTemplate = MakoTemplate(filename=fullServletPath, lookup=templateLookup, module_directory=self.servletContainer.tempDir)

        self._manifestEntry = manifestEntry

        self._sourceChangeCallback = sourceChangeCallback

        self._fileWatcher = FileWatcher(fullServletPath, lambda path: self._sourceChangeCallback(self))

        self._fileWatcher.start()

    def __str__(self):
        return str(self._manifestEntry)

    def unload(self):
        self._fileWatcher.stop()

    @property
    def manifestEntry(self):
        return self._manifestEntry

    @property
    def servletContainer(self):
        return self._servletContainer

    def handleRequest(self, request, response):
        response.sendResponse(CODE_OK)

        response.sendHeader(HDR_CONTENT_TYPE, MIME_HTML)

        self._makoTemplate.render_context(Context(response, request=request, response=response, **self._servletContainer.env))

        return True
