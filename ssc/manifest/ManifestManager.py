import logging

from ssc.manifest.PageEntry import PageEntry
from ssc.utils.FileWatcher import FileWatcher


logger = logging.getLogger(__name__)

class ManifestManager:
    MANIFEST_DICT_NAME = 'manifest'

    PAGES_KEY_NAME = 'pages'
    PAGE_404_KEY_NAME = '404_page'
    PAGE_FILE_KEY_NAME = 'file'
    PAGE_PATTERN_KEY_NAME = 'pattern'

    def __init__(self, manifestPath, onPageAdded=None, onPageRemoved=None, onPageChanged=None, onManifestUpdated=None):
        # Manifest file path (relative to container root)
        self._manifestPath = manifestPath

        # Callback called when a new page manfiest entry has been added
        self._onPageAdded = onPageAdded

        # Callback called when servlet page entry has been removed
        self._onPageRemoved = onPageRemoved

        # Callback called when servlet page entry has been changed
        self._onPageChanged = onPageChanged

        self._onManifestUpdated = onManifestUpdated

        # List of page manifest entries
        self._pages = []

        # Start watching manifest file
        self._manfiestWatch = FileWatcher(self._manifestPath, lambda path: self._onManifestChanged())
        self._manfiestWatch.start()

        self._page404 = None
        self._favIco = None

        # Run initial parse
        self._onManifestChanged()

    def stop(self):
        self._manfiestWatch.stop()

    def _onManifestChanged(self):
        '''
        Called when manifest file content has been changed
        '''

        logger.debug('Updating manifest')


        # Try reading manfiest from file
        try:
            manifest = self._readManifest()
        except Exception as e:
            logger.error('Error reading manifest: %r' % str(e))

            return


        # Generate a list of new pages from manifest
        newPages = []
        for i in manifest[ManifestManager.PAGES_KEY_NAME]:
            pageFile = i[ManifestManager.PAGE_FILE_KEY_NAME]
            pagePattern = i[ManifestManager.PAGE_PATTERN_KEY_NAME] if ManifestManager.PAGE_PATTERN_KEY_NAME in i else None
            newPages.append(PageEntry(pageFile, pagePattern))

        # Check if any pages have been deleted
        tmp = []

        for oldPage in self._pages:
            pageExists = False

            for newPage in newPages:
                if newPage.filePath == oldPage.filePath:
                    pageExists = True
                    break

            if not pageExists:
                # Page deleted
                self._onPageRemoved(oldPage)
            else:
                tmp.append(oldPage)

        self._pages = tmp

        # Check for changed entries and added pages
        for newPage in newPages:
            oldPage = self._findPageByFile(newPage.filePath)

            if oldPage and newPage != oldPage:
                # Replace old entry with new
                oldIndex = self._pages.index(oldPage)

                self._pages[oldIndex] = newPage

                self._onPageChanged(newPage)

            elif not oldPage:
                # New page
                self._pages.append(newPage)

                self._onPageAdded(newPage)

        # Check special pages
        self._page404 = manifest[ManifestManager.PAGE_404_KEY_NAME] if ManifestManager.PAGE_404_KEY_NAME in manifest else None
        if not self._page404:
            logger.warning('page 404 not found')

        logger.debug('Manifest processed')

        if self._onManifestUpdated:
            self._onManifestUpdated(self)

    def _readManifest(self):
        '''
        Reads manfiest and updates page entry list
        '''

        manifestLocals = {}
        manifestGlobals = {}

        with open(self._manifestPath, 'r') as fileObj:
            manifestCode = fileObj.read()

            code = compile(manifestCode, self._manifestPath, 'exec')

            exec(code, manifestLocals, manifestGlobals)

        if ManifestManager.MANIFEST_DICT_NAME not in manifestGlobals:
            raise RuntimeError('%r dictionary missing from manifest' % ManifestManager.MANIFEST_DICT_NAME)

        manifest = manifestGlobals[ManifestManager.MANIFEST_DICT_NAME]

        if ManifestManager.PAGES_KEY_NAME not in manifest:
            raise RuntimeError('Pages list missing from manfiest')

        return manifest

    def _findPageByFile(self, filePath):
        for page in self._pages:
            if filePath == page.filePath:
                return page
        return None

    @property
    def page404(self):
        return self._page404
