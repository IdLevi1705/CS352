import threading
import time
import random

import socket
# tsc - TS connection
from collections import OrderedDict


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
    raw_file = open('PROJI-DNSTS.txt', 'r')
    DNS_TSTable = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if not temp_split[0] in DNS_TSTable:
            DNS_TSTable[temp_split[0]] = line_num
    raw_file.close()

    while True:
        data_from_client = csockid.recv(3074).decode('utf-8')
        if data_from_client.strip() in DNS_TSTable:
            p = DNS_TSTable.get(data_from_client.strip())
            f = open('PROJI-DNSTS.txt', 'r')
            return_line = f.readlines()[p].strip()
            csockid.send(return_line.encode('utf-8'))
        else:
            # go and look if you can find it in TS server!
            return_message = str(data_from_client) + '-' + 'NS'
            csockid.send(return_line.encode('utf-8'))
        if data_from_client == "":
            break


thread3 = threading.Thread(name='TSserver', target=TSserver)
thread3.start()
time.sleep(random.random() * 5)
