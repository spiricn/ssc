import logging


class Logger:
    LEVEL_VERBOSE, \
    LEVEL_DEBUG, \
    LEVEL_INFO, \
    LEVEL_WARNING, \
    LEVEL_ERROR, \
    LEVEL_FATAL = range(6)

    LOGGING_FORMAT = '[%(asctime)-15s %(tag)-6s]: %(message)s'

    def __init__(self, parentObj):
        self._tag = parentObj.__class__.__name__

        self._logger = logging.getLogger(self._tag)

    @staticmethod
    def initLogging():
        logging.basicConfig(format=Logger.LOGGING_FORMAT, level=logging.DEBUG)

    def v(self, *args, **kwargs):
        self._log(Logger.LEVEL_VERBOSE, *args, **kwargs)

    def d(self, *args, **kwargs):
        self._log(Logger.LEVEL_DEBUG, *args, **kwargs)

    def i(self, *args, **kwargs):
        self._log(Logger.LEVEL_INFO, *args, **kwargs)

    def w(self, *args, **kwargs):
        self._log(Logger.LEVEL_WARNING, *args, **kwargs)

    def e(self, *args, **kwargs):
        self._log(Logger.LEVEL_ERROR, *args, **kwargs)

    def f(self, *args, **kwargs):
        self._log(Logger.LEVEL_FATAL, *args, **kwargs)

    def _log(self, level, *args, **kwargs):
        message = ''

        for i in args:
            message += i

        { Logger.LEVEL_VERBOSE : self._logger.debug,
          Logger.LEVEL_DEBUG : self._logger.debug,
          Logger.LEVEL_INFO : self._logger.info,
          Logger.LEVEL_WARNING : self._logger.warning,
          Logger.LEVEL_ERROR : self._logger.error,
          Logger.LEVEL_FATAL : self._logger.critical,
        }[level](message, extra={'tag' : self._tag})
