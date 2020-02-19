import threading
import time
import random
import socket


def RSserver():
    try:
        rsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50111)
    rsc.bind(server_binding)
    rsc.listen(1)
    host = socket.gethostname()
    # print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    # print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = rsc.accept()
    # print ("[S]: Got a connection request from a client at {}".format(addr))
    # while True:
    data_from_client = csockid.recv(3074).encode('utf-8')
    print(data_from_client)
        #
        # rsc.close()


RSserver()

    # # Close the server socket
    # rsc.close()
    # exit()
