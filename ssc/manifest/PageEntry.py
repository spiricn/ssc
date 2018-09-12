class PageEntry(object):
    def __init__(self, filePath, pattern):
        self._filePath = filePath
        self._pattern = pattern

    @property
    def filePath(self):
        '''
        Servlet path relative to container root directory
        '''
        return self._filePath

    @property
    def pattern(self):
        '''
        List of regex expressions used to pair servlets with URLs
        '''

        return self._pattern

    @filePath.setter
    def filePath(self, value):
        self._filePath = value

    def __eq__(self, other):
        if isinstance(other, PageEntry):
            return self._pattern == other._pattern and self._filePath == other._file
        else:
            return False

    def __neq__(self, other):
        return not (self == other)

    def __str__(self):
        return '{ManifestEntry: file=%r ; pattern=%r }' % (self._filePath, self._pattern)
