import threading
import time
import random
import sys
import socket


def client_connection():
    # client_LS_connection - opens socket for RS server.
    try:
        client_LS_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created for [RS] server")
    except socket.error as err:
        print('ERROR! Socket open error: {}\n'.format(err))

    # if len(sys.argv) < 3:
    #     print('============================================================================================== \n')
    #     print("[You have missed one of the arguments, please make sure you type in: lsHostname, lsListenPort] \n")
    #     print('============================================================================================== \n')
    #     sys.exit()

    # receives data from user - using command line arguments.
    # 1. host name.
    # 2. port for LS server.
    ls_hostname_input = 'localhost'
    # ls_hostname_input = sys.argv[1]
    ls_listen_port = 50006
    # ls_listen_port = int(sys.argv[2])

    I_P = socket.gethostbyname(ls_hostname_input)
    print("[C]: This client running on IP address {}".format(I_P))
    # connect to the server on local machine
    server_binding = (I_P, ls_listen_port)
    client_LS_connection.connect(server_binding)

    # open query_source and start sending them to LS server ONLY.
    open_file = open('PROJ2-HNS.txt', 'r')
    result_file = open('RESOLVED.txt', 'w')
    # start reading lines from PROJ2-HNS.txt file where all the addresses are store and waiting to be queried.
    for line in open_file:
        if '\n' in line:
            line = line[:-1]
        # address is ready to be sent to [RS] server first.
        client_LS_connection.send(line.encode('utf-8'))
        print("Line from HNS file -> ", line)
        s = client_LS_connection.recv(3024).encode('utf-8')
        print(s)
        result_file.write(str(s))
        result_file.write('\n')

    client_LS_connection.send("".encode('utf-8'))


thread1 = threading.Thread(name='client_connection', target=client_connection)
thread1.start()
