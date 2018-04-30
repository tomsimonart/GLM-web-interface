import json
import argparse
import selectors
import threading
import multiprocessing
from os import path
from GLM import glm
from time import sleep
from queue import Queue, Empty
from GLM.source.libs.rainbow import msg

BUFFSIZE = 512

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

def setup():
    """Sets up the argument parser
    """
    parser = argparse.ArgumentParser(description="Serve GLM")
    parser.add_argument('--host', help='Host', default='localhost', type=str)
    parser.add_argument('--port', '-p', help='Port', default=9999, type=int)
    parser.add_argument(
        '--verbose', '-v', action='count', help='Verbose level', default=0
        )
    parser.add_argument(
        '--sverbose', '-V', help='Special verbosity', action='append', type=str
        )
    parser.add_argument(
        '--matrix', '-m', help='Matrix enabled', action='store_true'
        )
    parser.add_argument('--show', '-s', help='Virtual matrix enabled',
    action='store_true')
    parser.add_argument(
        '--guishow', '-g', help='GUI enabled', action='store_true'
        )

    args = parser.parse_args()

    dir = path.dirname(__file__)
    rel_path = path.join(dir, 'GLM/verbosity')

    with open(rel_path, 'w') as f:
        f.write(str(args.verbose)+'\n')
        if args.sverbose is not None:
            for arg in args.sverbose:
                f.write(arg+'\n')

    server_addr = (args.host, args.port)


if __name__ == "__main__":
    setup()
