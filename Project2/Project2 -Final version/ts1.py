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

    port_from_command_line_TS = int(sys.argv[1])
    ser_bind = ('', port_from_command_line_TS)
    ts1_sock.bind(ser_bind)
    ts1_sock.listen(1)
    # ts1_ls_conn: connection socket with ls server
    ts1_ls_conn, addr = ts1_sock.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))

    # send a intro message to the client.
    raw_file = open('PROJ2-DNSTS1.txt', 'r')
    DNS_TST1able = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if not temp_split[0] in DNS_TST1able:
            DNS_TST1able[temp_split[0]] = line_num
    raw_file.close()

    return_msg = ''

    while True:
        data_from_client = ts1_ls_conn.recv(1024).decode('utf-8')
        if len(data_from_client) == 0:
            break
        if data_from_client in DNS_TST1able:
            raw = open('PROJ2-DNSTS1.txt', 'r')
            p = DNS_TST1able.get(data_from_client.strip())
            return_line = raw.readlines()[p].strip()
            return_msg = return_line
            ts1_ls_conn.send(return_msg.encode('utf-8'))
            raw.close()


thread3 = threading.Thread(name='TS1_server', target=TS1_server)
thread3.start()
time.sleep(random.random() * 5)
