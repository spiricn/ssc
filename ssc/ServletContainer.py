import os

from ssc.Logger import Logger
from ssc.ManifestManager import ManifestManager
from ssc.Servlet import Servlet


class ServletContainer:
    '''
    Parent class of all the servlets
    '''

    MANIFEST_FILE_NAME = 'Manifest.py'

    def __init__(self, server, directoryPath):
        self._log = Logger(self)

        # Servlet directory path
        self._directoryPath = directoryPath

        # Reference to parent HTTP server
        self._server = server

        # List of all loaded servlets
        self._servlets = []

        # Full manifest file path
        self._manifestPath = os.path.join(self._directoryPath, ServletContainer.MANIFEST_FILE_NAME)

        self._manifestManager = ManifestManager(self, self._manifestPath, self._onServletAdded, self._onServletRemoved, self._onServletChanged)

        self._log.d('Servlet container initialized')

    @property
    def rootDir(self):
        return self._directoryPath

    def _onServletSourceChanged(self, servlet):
        self._reloadServlet(servlet.manifestEntry)

    def _findServlet(self, file):
        '''
        Finds servlet with given name
        '''

        for i in self._servlets:
            if i.manifestEntry.file == file:
                return i

        return None

    def _unloadServlet(self, manifestEntry):
        '''
        Unloads servlet
        '''

        servlet = self._findServlet(manifestEntry.file)

        servlet.unload()

        self._servlets.remove(servlet)

    def _loadServlet(self, manifestEntry):
        '''
        Adds a new servlet
        '''

        # Full servlet path
        path = os.path.join(self._directoryPath, manifestEntry.file)

        if not os.path.exists(path):
            self._log.e('Could not find servlet file specified by manifest: %r' % path)

            return

        # Unload old version of servlet if possible
        oldServlet = self._findServlet(manifestEntry.file)

        if oldServlet:
            self._unloadServlet(oldServlet)

        servlet = Servlet(self, manifestEntry, self._onServletSourceChanged)

        self._servlets.append(servlet)

    def _reloadServlet(self, manifestEntry):
        self._unloadServlet(manifestEntry)

        self._loadServlet(manifestEntry)

    def _onServletAdded(self, manifestEntry):
        try:
            self._loadServlet(manifestEntry)

            self._log.d('Servlet loaded: %r' % manifestEntry.file)
        except Exception as e:
            self._log.e('Error loading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _onServletRemoved(self, manifestEntry):
        try:
            self._unloadServlet(manifestEntry)

            self._log.d('Servlet unloaded: %r' % manifestEntry.file)
        except Exception as e:
            self._log.e('Error unloading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _onServletChanged(self, manifestEntry):
        try:
            self._reloadServlet(manifestEntry)

            self._log.d('Servlet reloaded: %r' % os.path.basename(manifestEntry.file))
        except Exception as e:
            self._log.e('Error unloading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _getServlet(self, request):
        if request.url.path == '/':
            pageHomeServlet = self._findServlet(self._manifestManager.pageHome)

            if not pageHomeServlet:
                self._log.e('Could not find home page servlet: %r' % self._manifestManager.pageHome)

            else:
                return pageHomeServlet

        for servlet in self._servlets:
            for i in servlet.regex:
                if i.match(request.url.path):
                    return servlet

        if self._manifestManager.page404Servlet:
            page404Servlet = self._findServlet(self._manifestManager.page404Servlet)

            if not page404Servlet:
                self._log.e('Could not find 404 servlet: %r' % self._manifestManager.page404)

            else:
                return page404Servlet

        return None

    def handleRequest(self, request, response):
        servlet = self._getServlet(request)

        if not servlet:
            response.sendResponse(404)

        else:
            servlet.handleRequest(request, response)
