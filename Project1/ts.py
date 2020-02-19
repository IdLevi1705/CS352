import threading
import time
import random

import socket
# tsc - TS connection

def TSserver():
    try:
        tsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50112)
    tsc.bind(server_binding)
    tsc.listen(1)
    host = socket.gethostname()
    # print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    # print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = tsc.accept()
    # print ("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    # while True:
    #
    #
    #
    # tsc.close()
    # exit()
