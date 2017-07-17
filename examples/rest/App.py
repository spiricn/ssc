import logging
from os.path import sys, os
from time import sleep

from ssc.http import HTTP
from ssc.servlets.RestServlet import RestHandler
from ssc.servlets.ServletContainer import ServletContainer


def sampleRest():
    return HTTP.CODE_OK, HTTP.MIME_TEXT, 'Hello world'

def streamer():
    numChunks = 10

    yield '<html><body>'

    for i in range(numChunks):
        yield '<p>Streaming chunk %d/%d</p>' % (i + 1, numChunks)

        sleep(0.5)

    yield '</body></html>'

def streamRest():
    return HTTP.CODE_OK, HTTP.MIME_HTML, streamer()

def main():
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG,
            format='%(levelname)s/%(name)s: %(message)s')
    logger = logging.getLogger(__name__)

    exampleDir = os.path.dirname(__file__)

    container = ServletContainer('', 8080, os.path.join(exampleDir, 'root'), os.path.join(exampleDir, 'tmp'))

    container.start()

    container.addRestAPI()

    container.rest.addHandler(RestHandler('sample', sampleRest, 'This is a sample help doc', chunked=False))

    container.rest.addHandler(RestHandler('stream', streamRest, 'This is a stream help doc', chunked=True))

    logger.debug('sample started')
    logger.debug('Try accessing http://localhost:8080/rest/sample from your browser for a simple REST call')
    logger.debug('Try accessing http://localhost:8080/rest/stream from your browser, for a chunked REST call')
    logger.debug('press [ENTER] to stop')

    input()

    container.stop()

    logger.debug('sample stopped')

    return 0


if __name__ == '__main__':
    sys.exit(main())
