import threading
import time
import random

import socket


def client_connection():
    # RS_connection - opens socket for RS server.
    # TS_connection - opens socket for TS server.
    # These two connections allow us to talk to two different servers at the same time.
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
    # start reading lines from PROJI-HNS.txt file where all the addresses are store and waiting to be queried.
    for line in open_file:
        if '\n' in line:
            line = line[:-1]
        # address is ready to be sent to [RS] server first.
        RS_connection.send(line.encode('utf-8'))

        receive_response = RS_connection.recv(1024).decode('utf-8')
        server_response = receive_response.split()
        # check the answer that [RS] server returns.
        # 1. If answer contains flag 'A' -> we have a mathc and we can go ahead and write it into RESOLVED.txt file.
        # 2. If no match, move to the next server which is given by the [RS]
        # server -> address for next server involves 'NS' flag.
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
            # Move to [TS] with hostname that was given by [RS] server.
            TS_connection.send(line.encode('utf-8'))
            ts_response = TS_connection.recv(1024).decode('utf-8')
            # Answer from TS will be written into RESOLVED.txt
            result_file.write(ts_response)
            result_file.write('\n')

    RS_connection.close()
    TS_connection.close()
    exit()


thread1 = threading.Thread(name='client_connection', target=client_connection)
thread1.start()
