import threading
import time
import random
import sys
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

    if len(sys.argv) < 4:
        print('============================================================================================== \n')
        print("[You have missed one of the arguments, please make sure you type in: HostName, RSPort, TSPort] \n")
        print('============================================================================================== \n')
        sys.exit()

    # receive data from user - using command line arguments.
    # 1. host name.
    # 2. port for RS server.
    # 3. port for TS server.
    port_from_command_line_Client_to_RS = int(sys.argv[2])
    port_from_command_line_Client_to_TS = int(sys.argv[3])
    host_name_from_command_line = str(sys.argv[1])
    host_addr = host_name_from_command_line
    local_IP = socket.gethostbyname(socket.gethostname())
    print("[C]: This client running on IP address {}".format(local_IP))
    # connect to the server on local machine
    server_binding = (host_addr, port_from_command_line_Client_to_RS)
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
                server_binding0 = (server_response[0], port_from_command_line_Client_to_TS)
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
