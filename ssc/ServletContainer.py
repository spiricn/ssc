import logging
import os

from ssc.FileServlet import FileServlet
from ssc.ManifestManager import ManifestManager
from ssc.PageServlet import PageServlet
from ssc.RestServlet import RestServlet
from ssc.HTTP import CODE_NOT_FOUND


logger = logging.getLogger(__name__)

class ServletContainer:
    '''
    Parent class of all the servlets
    '''

    MANIFEST_FILE_NAME = 'Manifest.py'

    def __init__(self, server, directoryPath, tempDir):
        # Servlet directory path
        self._directoryPath = os.path.realpath(directoryPath)

        self._tempDir = os.path.realpath(tempDir)

        if not os.path.isdir(self._tempDir):
            os.makedirs(self._tempDir)

        # Reference to parent HTTP server
        self._server = server

        # List of all loaded servlets
        self._servlets = []

        # Full manifest file path
        self._manifestPath = os.path.join(self._directoryPath, ServletContainer.MANIFEST_FILE_NAME)

        self._manifestManager = ManifestManager(self, self._manifestPath, self._onServletAdded, self._onServletRemoved, self._onServletChanged)

        self._fileServlet = FileServlet(self)

        self._env = {}

        logger.debug('Servlet container initialized')

    def addRestAPI(self, pattern='^\\/rest\\/'):
        self._restServlet = RestServlet(self, pattern)

        self.addServlet(self._restServlet)

    @property
    def rest(self):
        return self._restServlet

    @property
    def env(self):
        return self._env

    @property
    def rootDir(self):
        return self._directoryPath

    @property
    def tempDir(self):
        return self._tempDir

    def _onServletSourceChanged(self, servlet):
        self._reloadServlet(servlet.manifestEntry)

    def _findServlet(self, file):
        '''
        Finds servlet with given name
        '''

        for i in self._servlets:
            if isinstance(i, PageServlet):
                if i.manifestEntry and i.manifestEntry.file == file:
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

        servlet = PageServlet(self, manifestEntry, self._onServletSourceChanged)

        self._servlets.append(servlet)

    def addServlet(self, servlet):
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
            if not servlet.regex:
                continue

            if servlet.regex.match(request.url.path):
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

        return response.sendResponse(CODE_NOT_FOUND)
