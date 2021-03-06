import logging
import os
import traceback

from ssc.http.HTTP import CODE_NOT_FOUND, CODE_INTERNAL_SERVER_ERROR
from ssc.http.ThreadedHTTPServer import ThreadedHTTPServer
from ssc.manifest.ManifestManager import ManifestManager
from ssc.servlets.FileServlet import FileServlet
from ssc.servlets.PageServlet import PageServlet
from ssc.servlets.RestServlet import RestServlet

logger = logging.getLogger(__name__)


class ServletContainer:
    '''
    Parent class of all the servlets
    '''

    MANIFEST_FILE_NAME = 'Manifest.py'

    def __init__(self, address, port, directoryPath, tempDir):
        # Servlet directory path
        self._directoryPath = os.path.realpath(directoryPath)

        self._tempDir = os.path.realpath(tempDir)

        if not os.path.isdir(self._tempDir):
            os.makedirs(self._tempDir)

        # Reference to parent HTTP server
        self._server = ThreadedHTTPServer(address, port, self.handleRequest)

        # List of all loaded servlets
        self._servlets = []

        # Full manifest file path
        self._manifestPath = os.path.join(self._directoryPath, ServletContainer.MANIFEST_FILE_NAME)

        self._manifestManager = ManifestManager(self._manifestPath,
                                                self._onServletAdded,
                                                self._onServletRemoved,
                                                self._onServletChanged)

        self._fileServlet = FileServlet(self)

        self._env = {}

        self._restServlet = None

        logger.debug('Servlet container initialized:\n Root: %r\n Tmp: %r' % (self._directoryPath, self._tempDir))

    def start(self):
        return self._server.start()

    def stop(self):
        self._manifestManager.stop()

        self._unloadServlets()

        return self._server.stop()

    def addRestAPI(self, pattern='^\\/rest\\/'):
        self._restServlet = RestServlet(self, pattern)

        self.addServlet(self._restServlet)

    @property
    def rest(self):
        if not self._restServlet:
            raise RuntimeError('Rest servlet not created, call "addRestAPI" first')

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

    def _findServlet(self, filePath):
        '''
        Finds servlet with given name
        '''

        for i in self._servlets:
            if isinstance(i, PageServlet):
                if i.manifestEntry and i.manifestEntry.filePath == filePath:
                    return i

        return None

    def _unloadServlets(self):
        while self._servlets:
            self._unloadSingleServlet(self._servlets[0])

    def _unloadServlet(self, manifestEntry):
        '''
        Unloads servlet
        '''
        self._unloadSingleServlet(self._findServlet(manifestEntry.filePath))

    def _unloadSingleServlet(self, servlet):
        servlet.unload()

        self._servlets.remove(servlet)

    def _loadServlet(self, manifestEntry):
        '''
        Adds a new servlet
        '''

        # Full servlet path
        path = os.path.join(self._directoryPath, manifestEntry.filePath)

        if not os.path.exists(path):
            logger.error('Could not find servlet file specified by manifest: %r' % path)

            return

        # Unload old version of servlet if possible
        oldServlet = self._findServlet(manifestEntry.filePath)

        if oldServlet:
            self._unloadServlet(oldServlet)

        servlet = PageServlet(self, manifestEntry, self._onServletSourceChanged)

        self._servlets.append(servlet)

    def insertServlet(self, index, servlet):
        self._servlets.insert(index, servlet)

    @property
    def servlets(self):
        return [i for i in self._servlets]

    def addServlet(self, servlet):
        self._servlets.append(servlet)

    def _reloadServlet(self, manifestEntry):
        self._unloadServlet(manifestEntry)

        self._loadServlet(manifestEntry)

    def _onServletAdded(self, manifestEntry):
        try:
            self._loadServlet(manifestEntry)

            logger.debug('Servlet loaded: %r' % manifestEntry.filePath)
        except Exception as e:
            logger.error('Error loading servlet %r: %r' % (manifestEntry.filePath, str(e)))

    def _onServletRemoved(self, manifestEntry):
        try:
            self._unloadServlet(manifestEntry)

            logger.debug('Servlet unloaded: %r' % manifestEntry.file)
        except Exception as e:
            logger.error('Error unloading servlet %r: %r' % (manifestEntry.filePath, str(e)))

    def _onServletChanged(self, manifestEntry):
        try:
            self._reloadServlet(manifestEntry)

            logger.debug('Servlet reloaded: %r' % os.path.basename(manifestEntry.filePath))
        except Exception as e:
            logger.error('Error unloading servlet %r: %r' % (manifestEntry.filePath, str(e)))

    def _getServlet(self, request):
        servlets = []

        for servlet in self._servlets:
            if not servlet.regex:
                continue

            if servlet.regex.match(request.url.path):
                servlets.append(servlet)

        if os.path.isfile(os.path.join(self._directoryPath, request.url.path[1:])):
            servlets.append(self._fileServlet)

        return servlets

    def handle404(self, request, response):
        page404Servlet = self._findServlet(self._manifestManager.page404)

        if not page404Servlet:
            logger.warning('Could not find 404 servlet: %r' % self._manifestManager.page404)

            response.sendResponse(CODE_NOT_FOUND)
            response.write('<html><head>404</head><body>Not found</body></html>')

            return True

        else:
            return page404Servlet.handleRequest(request, response)

    def handle500(self, request, response):
        response.sendResponse(CODE_INTERNAL_SERVER_ERROR)
        response.write('<html><head>500</head><body>Internal server error</body></html>')

        return True

    def handleRequest(self, request, response):
        servlets = self._getServlet(request)

        for servlet in servlets:
            try:
                if servlet.handleRequest(request, response):
                    return True
            except Exception:
                logger.error('Exception occurred while handling servlet: %s' % traceback.format_exc())
                return True

        return self.handle404(request, response)
