import threading
import time
import random
import socket
import sys
from collections import OrderedDict


def RSserver():
    try:
        rsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    port_from_command_line = int(sys.argv[1])
    server_binding = ('', port_from_command_line)
    rsc.bind(server_binding)
    rsc.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = rsc.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))
    # store data in HashTable -> orderedDict()
    raw_file = open('PROJI-DNSRS.txt', 'r')
    DNS_Table = OrderedDict()
    for line_num, data_line in enumerate(raw_file, 0):
        temp_split = data_line.split(' ')
        if (temp_split[2]).strip() == 'NS':
            DNS_Table['NS'] = line_num
            continue
        if not temp_split[0] in DNS_Table:
            DNS_Table[temp_split[0]] = line_num
    raw_file.close()
    return_message = ''

    while True:
        data_from_client = csockid.recv(1024).decode('utf-8')
        if data_from_client.strip() in DNS_Table:
            f = open('PROJI-DNSRS.txt', 'r')
            p = DNS_Table.get(data_from_client.strip())
            return_line = f.readlines()[p].strip()
            return_message = return_line
        else:
            f = open('PROJI-DNSRS.txt', 'r')
            p1 = DNS_Table.get('NS')
            return_line1 = f.readlines()[p1].strip()
            return_message = return_line1
        if data_from_client == "":
            break
        print('[S]: Message from RS server {}'.format(return_message))
        csockid.send(return_message.encode('utf-8'))

    f.close()
    rsc.close()
    exit()


thread2 = threading.Thread(name='RSserver', target=RSserver)
thread2.start()
time.sleep(random.random() * 5)
