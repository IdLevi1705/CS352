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

    lsListenPort = int(sys.argv[1])
    server_client_binding = ('', lsListenPort)
    LS_Server.bind(server_client_binding)
    LS_Server.listen(1)
    # c_l_c: client -> ls connection
    c_l_c, addr = LS_Server.accept()

    ts1Hostname = sys.argv[2]
    host_name_TS1 = socket.gethostbyname(ts1Hostname)
    ts1ListenPort = int(sys.argv[3])
    LS_TS1_binding = (host_name_TS1, ts1ListenPort)
    TS1_connection.connect(LS_TS1_binding)
    print("Connection with TS1 has been established")

    ts2Hostname = str(sys.argv[4])
    host_name_TS2 = socket.gethostbyname(ts2Hostname)
    ts2ListenPort = int(sys.argv[5])
    LS_TS2_binding = (host_name_TS2, ts2ListenPort)
    TS2_connection.connect(LS_TS2_binding)
    print("Connection with TS2 has been established")

    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))

    print("[S]: Got a connection request from a client at {}".format(addr))
    err_msg = ' - Error:HOST NOT FOUND'

    while True:
        data_from_client = c_l_c.recv(1024).decode('utf-8')
        if len(data_from_client) == 0:
            disconnect_from_servers(TS1_connection, TS2_connection)
            break
        send_msg_to_servers(TS1_connection, TS2_connection, data_from_client)
        # This process is a system call that checks which server returns something at a time if
        # neither return it will wait 5 sec and then returns nothing.
        reader, _, _ = select.select([TS1_connection, TS2_connection], [], [], float(5))
        for r in reader:
            if r is TS1_connection:
                msg_ts1 = TS1_connection.recv(1024).decode('utf-8')
                c_l_c.send(msg_ts1.encode('utf-8'))
            if r is TS2_connection:
                msg_ts2 = TS2_connection.recv(1024).decode('utf-8')
                c_l_c.send(msg_ts2.encode('utf-8'))
        if not (reader or _ or _):
            c_l_c.send((data_from_client + err_msg).encode('utf-8'))


# disconnect from all server - just a method to shut down the servers and the process is done.
def disconnect_from_servers(server_ts1, server_ts2):
    server_ts1.send("".encode('utf-8'))
    server_ts2.send("".encode('utf-8'))


# send message from client to servers TS1 and TS2 to execute the lookup process.
def send_msg_to_servers(server_ts1, server_ts2, data):
    server_ts1.send(data.encode('utf-8'))
    server_ts2.send(data.encode('utf-8'))


thread2 = threading.Thread(name='LSServer', target=LSServer)
thread2.start()
time.sleep(random.random() * 5)
