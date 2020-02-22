import threading
import time
import random
import socket
from collections import OrderedDict


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
    print ("[S]: Got a connection request from a client at {}".format(addr))
    # store data in HashTable -> orderedDict()
    raw_file = open('PROJI-DNSRS.txt', 'r')
    DNS_Table = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if not temp_split[0] in DNS_Table:
            DNS_Table[temp_split[0]] = line_num
    raw_file.close()

    # how to stop the streaming and receive one word at the time.....

    while True:
        data_from_client = csockid.recv(3074).decode('utf-8')
        if data_from_client.strip() in DNS_Table:
            p = DNS_Table.get(data_from_client.strip())
            f = open('PROJI-DNSRS.txt', 'r')
            return_line = f.readlines()[p].strip()
            csockid.send(return_line.encode('utf-8'))
        else:
            csockid.send(str(data_from_client.strip()).encode('utf-8'))
        if data_from_client == "":
            break

        # rsc.close()
        # exit()


t2 = threading.Thread(name='RSserver', target=RSserver)
t2.start()
time.sleep(random.random() * 5)
