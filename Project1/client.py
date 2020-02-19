import threading
import time
import random

import socket


# crs - connection with rs server
# cts - connection with ts server

def client_connection():
    try:
        crs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))
        exit()

    port = 50111
    host_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (host_addr, port)
    crs.connect(server_binding)

    # open query_source and start sending them to RS server first if it not found go to TS server.
    query_source = 'PROJI-HNS.txt'
    open_file = open(query_source, 'r')
    # ignore '/n'
    for line in open_file:
        if '\n' in line:
            line = line[:-1]
        crs.send(line.encode('utf-8'))
        print(crs.send(line.encode('utf-8')))






    # crs.close()
    # exit()
    #
t1 = threading.Thread(name='client_connection', target=client_connection)
t1.start()
    #
    # exit()
