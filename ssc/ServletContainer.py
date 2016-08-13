import logging
import os

from ssc.ManifestManager import ManifestManager
from ssc.Servlet import Servlet
from ssc.FileServlet import FileServlet


logger = logging.getLogger(__name__)

class ServletContainer:
    '''
    Parent class of all the servlets
    '''

    MANIFEST_FILE_NAME = 'Manifest.py'

    def __init__(self, server, directoryPath):
        # Servlet directory path
        self._directoryPath = os.path.realpath(directoryPath)

        # Reference to parent HTTP server
        self._server = server

        # List of all loaded servlets
        self._servlets = []

        # Full manifest file path
        self._manifestPath = os.path.join(self._directoryPath, ServletContainer.MANIFEST_FILE_NAME)

        self._manifestManager = ManifestManager(self, self._manifestPath, self._onServletAdded, self._onServletRemoved, self._onServletChanged)

        self._fileServlet = FileServlet(self)

        logger.debug('Servlet container initialized')

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
            logger.error('Could not find servlet file specified by manifest: %r' % path)

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

            logger.debug('Servlet loaded: %r' % manifestEntry.file)
        except Exception as e:
            logger.error('Error loading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _onServletRemoved(self, manifestEntry):
        try:
            self._unloadServlet(manifestEntry)

            logger.debug('Servlet unloaded: %r' % manifestEntry.file)
        except Exception as e:
            logger.error('Error unloading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _onServletChanged(self, manifestEntry):
        try:
            self._reloadServlet(manifestEntry)

            logger.debug('Servlet reloaded: %r' % os.path.basename(manifestEntry.file))
        except Exception as e:
            logger.error('Error unloading servlet %r: %r' % (manifestEntry.file, str(e)))

    def _getServlet(self, request):
        if request.url.path == '/':
            pageHomeServlet = self._findServlet(self._manifestManager.pageHome)

            if not pageHomeServlet:
                logger.error('Could not find home page servlet: %r' % self._manifestManager.pageHome)

            else:
                return pageHomeServlet

        for servlet in self._servlets:
            for i in servlet.regex:
                if i.match(request.url.path):
                    return servlet

        if os.path.isfile(os.path.join(self._directoryPath, request.url.path[1:])):
            return self._fileServlet

        if self._manifestManager.page404:
            page404Servlet = self._findServlet(self._manifestManager.page404)

            if not page404Servlet:
                logger.error('Could not find 404 servlet: %r' % self._manifestManager.page404)

            else:
                return page404Servlet

        return None

    def _handleFile(self, request, response):
        pass

    def handleRequest(self, request, response):
        servlet = self._getServlet(request)
        if servlet:
            return servlet.handleRequest(request, response)

        return response.sendResponse(404)
