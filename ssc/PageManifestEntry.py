class PageManifestEntry(object):
    def __init__(self, file, pattern):
        self._file = file

        self._pattern = pattern

    @property
    def file(self):
        '''
        Servlet path relative to container root directory
        '''
        return self._file

    @property
    def pattern(self):
        '''
        List of regex expressions used to pair servlets with URLs
        '''

        return self._pattern

    @file.setter
    def file(self, value):
        self._file = value

    def __eq__(self, other):
        if isinstance(other, PageManifestEntry):
            return self._pattern == other._pattern and self._file == other._file
        else:
            return False

    def __neq__(self, other):
        return not (self == other)
