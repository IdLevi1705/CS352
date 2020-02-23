import threading
import time
import random

import socket


def client_connection():
    try:
        RS_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created for [RS] server")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))
    try:
        TS_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created for [TS] server")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))

    port = 50111
    host_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (host_addr, port)
    RS_connection.connect(server_binding)
    connection = False
    # open query_source and start sending them to RS server first if it not found go to TS server.
    open_file = open('PROJI-HNS.txt', 'r')
    result_file = open('RESOLVED.txt', 'w')

    for line in open_file:
        if '\n' in line:
            line = line[:-1]
        RS_connection.send(line.encode('utf-8'))

        receive_response = RS_connection.recv(1024).decode('utf-8')
        server_response = receive_response.split()
        if server_response[2] == 'A':
            print('[C]: IP Found for address - {}'.format('['+receive_response+']'))
            result_file.write(str(receive_response))
            result_file.write('\n')
        if server_response[2] == 'NS':
            print('[C]: IP NOT Found TSHostname - NS {}'.format('['+receive_response+']'))
            if not connection:
                server_binding0 = (server_response[0], 50221)
                TS_connection.connect(server_binding0)
                connection = True

            TS_connection.send(line.encode('utf-8'))
            ts_response = TS_connection.recv(1024).decode('utf-8')
            result_file.write(ts_response)
            result_file.write('\n')

    RS_connection.close()
    TS_connection.close()
    exit()


thread1 = threading.Thread(name='client_connection', target=client_connection)
thread1.start()
