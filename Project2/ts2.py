import threading
import time
import random
import sys
import socket

from collections import OrderedDict


# tsc - TS connection

def TS2_server():
    try:
        ts2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    port_from_command_line_TS = 50008
    # port_from_command_line_TS = int(sys.argv[1])
    ser_bind = ('', port_from_command_line_TS)
    ts2_sock.bind(ser_bind)
    ts2_sock.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ts2_sock.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    raw_file = open('PROJ2-DNSTS2.txt', 'r')
    DNS_TSTable = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if not temp_split[0] in DNS_TSTable:
            DNS_TSTable[temp_split[0]] = line_num
    raw_file.close()
    print(DNS_TSTable)
    return_msg = ''

    while True:
        data_from_client = csockid.recv(1024).decode('utf-8')
        print(data_from_client)
        if data_from_client.strip() in DNS_TSTable:
            p = DNS_TSTable.get(data_from_client.strip())
            print(p)
            raw = open('PROJ2-DNSTS2.txt', 'r')
            return_line = raw.readlines()[p].strip()
            print(return_line)
            return_msg = return_line
            print("Yes")
            csockid.send(return_msg.encode('utf-8'))
            raw.close()
        else:
            print("NO")
            exit()


thread4 = threading.Thread(name='TS2_server', target=TS2_server)
thread4.start()
time.sleep(random.random() * 5)
