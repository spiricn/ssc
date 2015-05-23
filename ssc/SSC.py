import argparse

from ssc.HTTPServer import HTTPServer
from ssc.Logger import Logger


def programMain():
    # Initialize logging
    Logger.initLogging()

    parser = argparse.ArgumentParser()

    parser.add_argument('root', help='Directory containing Manfiest.py file and all the servlets')

    parser.add_argument('port', help='HTTP server port')

    args = parser.parse_args()

    server = HTTPServer(args.root, int(args.port))

    return server.start()

if __name__ == '__main__':
    exit(programMain())
