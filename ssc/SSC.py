import argparse
import logging

from ssc.HTTPServer import HTTPServer


def programMain():
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG,
            format='%(levelname)s/%(name)s: %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument('root', help='Directory containing Manfiest.py file and all the servlets')

    parser.add_argument('port', help='HTTP server port')

    args = parser.parse_args()

    server = HTTPServer(args.root, int(args.port))

    return server.start()

if __name__ == '__main__':
    exit(programMain())
