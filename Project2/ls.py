import threading
import time
import random
import socket
import sys
from collections import OrderedDict
import select


def LSServer():
    try:
        LS_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created for LSServer")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))

    try:
        TS1_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created for TS1 ")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))

    try:
        TS2_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created for TS2")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))

    port_from_command_line = int(sys.argv[1])
    host_name_TS1 = str(sys.argv[2])
    port_TS1 = int(sys.argv[3])
    host_name_TS2 = str(sys.argv[4])
    port_TS2 = int(sys.argv[5])
    # connection with client.
    server_client_binding = ('', port_from_command_line)
    LS_Server.bind(server_client_binding)
    LS_Server.listen(1)
    # connection with TS1
    LS_TS1_binding = (host_name_TS1, port_TS1)
    # connection with TS2
    LS_TS2_binding = (host_name_TS2, port_TS2)
    TS1_connection.connect(LS_TS1_binding)
    TS2_connection.connect(LS_TS2_binding)

    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = LS_Server.accept()
    ts1sockid, addrts1 = TS1_connection.accept()
    ts2sockid, addrts2 = TS2_connection.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))
    # store data in HashTable -> orderedDict()

    while True:
        # send to TS1 and TS2
        data_from_client = csockid.recv(1024).decode('utf-8')
        a = ts1sockid.send(data_from_client.encode('utf-8'))
        b = ts2sockid.send(data_from_client.encode('utf-8'))
        readers, _, _ = select.select([data_from_client], [a, b], [], [5])
        # send to TS1 and TS2
        csockid.send(return_message.encode('utf-8'))

    f.close()
    LS_Server.close()
    exit()


thread2 = threading.Thread(name='LSServer', target=LSServer)
thread2.start()
time.sleep(random.random() * 5)
