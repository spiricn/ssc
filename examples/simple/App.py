import logging
from os.path import sys, os

from ssc.servlets.ServletContainer import ServletContainer


def main():
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG,
            format='%(levelname)s/%(name)s: %(message)s')
    logger = logging.getLogger(__name__)

    exampleDir = os.path.dirname(__file__)

    container = ServletContainer('', 8080, os.path.join(exampleDir, 'root'), os.path.join(exampleDir, 'tmp'))

    container.start()

    logger.debug('sample started')
    logger.debug('Try accessing http://localhost:8080 from your browser')
    logger.debug('press [ENTER] to stop')

    input()

    container.stop()

    logger.debug('sample stopped')

    return 0


if __name__ == '__main__':
    sys.exit(main())
