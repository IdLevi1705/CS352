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
        TS1_connection.setblocking(True)
        print("[S]: Server socket created for TS1 ")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))

    try:
        TS2_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TS2_connection.setblocking(True)
        print("[S]: Server socket created for TS2")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))

    """ 
     python client.py 'localhost 50006'
    """
    port_from_command_line = 50006
    # port_from_command_line = int(sys.argv[1])
    TS_hostname = 'localhost'
    # TS_hostname = sys.argv[2]
    host_name_TS1 = socket.gethostbyname(TS_hostname)
    port_TS1 = 50007
    # port_TS1 = int(sys.argv[3])
    LS_TS1_binding = (host_name_TS1, port_TS1)
    TS1_connection.connect(LS_TS1_binding)
    print("Connection with TS1 established")
    # port_TS1 = int(sys.argv[3])
    host_name_TS2 = 'localhost'
    # host_name_TS2 = str(sys.argv[4])
    port_TS2 = 50008
    # port_TS2 = int(sys.argv[5])
    # connection with client.
    server_client_binding = ('', port_from_command_line)
    LS_Server.bind(server_client_binding)
    LS_Server.listen(1)
    csockid, addr = LS_Server.accept()
    # connection with TS1
    # LS_TS1_binding = (host_name_TS1, port_TS1)
    # connection with TS2
    LS_TS2_binding = (host_name_TS2, port_TS2)

    TS2_connection.connect(LS_TS2_binding)

    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))

    # ts2sockid, addrts2 = TS2_connection.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))
    msg = "Yup"
    while True:
        data_from_client = csockid.recv(1024).decode('utf-8')
        print("data received from client")
        TS1_connection.send(data_from_client.encode('utf-8'))
        print("data sent to TS1")
        TS2_connection.send(data_from_client.encode('utf-8'))
        print("data sent to TS2")
        reader, _, _ = select.select([TS1_connection, TS2_connection], [], [],)
        for r in reader:
            print("I entered r")
            if r is TS1_connection:
                bobok = TS1_connection.recv(1024).decode('utf-8')
                print("This is r -> ", bobok)
                csockid.send(bobok.encode('utf-8'))
            elif r is TS2_connection:
                bobok = TS2_connection.recv(1024).decode('utf-8')
                csockid.send(bobok.encode('utf-8'))

        print("Data from client - >>> ", data_from_client)

        # print("data received from TS1")
        # TS2_connection.recv(1024).decode('utf-8')
        # print("data received from TS2")
        # # a = ts1sockid.send(data_from_client.encode('utf-8'))

        # f.close()
        # LS_Server.close()
        # exit()


thread2 = threading.Thread(name='LSServer', target=LSServer)
thread2.start()
time.sleep(random.random() * 5)
