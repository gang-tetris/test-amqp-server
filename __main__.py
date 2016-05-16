from sys import argv
from src.server import Server

hostname = 'Logic'
if len(argv) > 1:
    hostname = argv[1]

server = Server(hostname)

