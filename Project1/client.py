import threading
import time
import random

import socket


# crs - connection with rs server
# cts - connection with ts server

def client_connection():
    try:
        RS_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))
    try:
        TS_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))

    port = 50111
    host_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (host_addr, port)
    RS_connection.connect(server_binding)

    # open query_source and start sending them to RS server first if it not found go to TS server.
    open_file = open('PROJI-HNS.txt', 'r')
    result_file = open('RESOLVED1.txt', 'w')

    for line in open_file:
        if '\n' in line:
            line = line[:-1]
        RS_connection.send(line.encode('utf-8'))

        receive_response = RS_connection.recv(3074)
        server_response = receive_response.split()
        print(server_response[1])
        if server_response[2] == 'A':
            result_file.write(str(receive_response))
            result_file.write('\n')
        else:
            port = 50112
            new_hostname = server_response[1]
            server_binding = (new_hostname, port)
            TS_connection.connect(server_binding)

            TS_connection.send(line.encode('utf-8'))
            ts_response = RS_connection.recv(3074)
            if str(ts_response) == 'err':
                print(ts_response)

    RS_connection.close()
    TS_connection.close()
    exit()


t1 = threading.Thread(name='client_connection', target=client_connection)
t1.start()
