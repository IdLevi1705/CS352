import threading
import time
import random
import sys
import socket

from collections import OrderedDict


# tsc - TS connection

def TS1_server():
    try:
        ts1_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    port_from_command_line_TS = 50007
    # port_from_command_line_TS = int(sys.argv[1])
    ser_bind = ('', port_from_command_line_TS)
    ts1_sock.bind(ser_bind)
    ts1_sock.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ts1_sock.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    raw_file = open('PROJ2-DNSTS1.txt', 'r')
    DNS_TSTable = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if not temp_split[0] in DNS_TSTable:
            DNS_TSTable[temp_split[0]] = line_num
    raw_file.close()
    return_msg = ''

    while True:
        data_from_client = csockid.recv(1024).decode('utf-8')
        if len(data_from_client) == 0:
            break
        if data_from_client in DNS_TSTable:
            raw = open('PROJ2-DNSTS1.txt', 'r')
            p = DNS_TSTable.get(data_from_client.strip())
            return_line = raw.readlines()[p].strip()
            return_msg = return_line
            csockid.send(return_msg.encode('utf-8'))
            raw.close()


thread3 = threading.Thread(name='TS1_server', target=TS1_server)
thread3.start()
time.sleep(random.random() * 5)
