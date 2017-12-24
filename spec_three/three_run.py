import socket
import json
import sys
import time
from pexpect import *
import select
def receive(fd,sock):
    s = fd.recv(6000)
    while 1:
        if 10 not in s:
            s = s + fd.recv(6000)
        else:
            break
#    print(s.decode('ascii'))
    return s
def run_spec(ip_and_port):
    fo = open("spec_three/1","r+")
    data = fo.read(3000)
    datalist = data.split('\n')
    print (len(datalist))
    for s in datalist:
        print(s)
    sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(4)]
    for i in range(4):
        try:
            sock[i].connect(ip_and_port)
        except:
            sock[i].close()
            print ("fd : ",i," fail.")


    worst = 0.0
    total = 0.0
    count = 0
    output = []
    timeout = 0.01
    for i in range (3):
        sock[i].send(((datalist[i])+'\n').encode('ascii'))
        s = receive(sock[i],sock)
    print('wait for 20 sec.')
    start_time = time.time()
    while 1:
        if int(time.time() - start_time) > 20:
            break
        readable, writable, exceptional = select.select(sock,output,sock,timeout);
        for fd in readable:
            tmp = receive(fd,sock)
            s = tmp.decode('ascii')
            print (s)
            if '127_0' in s:
                count = count + 1
            if '127_1' in s:
                count = count - 1
            if '127_2' in s:
                count = count + 1
    print('count = ',count)
    if count == 2:
        print ('correct')
        sock[3].send(((datalist[1])+'\n').encode('ascii'))
        s = receive(sock[3],sock)
        print ('closing fd')
        time.sleep(1.0)
        for i in range(4):
            sock[i].close()
            time.sleep(0.2)
        print('You should try another spec immediately without closing the server.')
        return
    else:
        print('Your server might crash or the matching does not correct.')
        print('ultra127_0 should match ultra127_2.')
        print('You can see the try_match data in spec_three/1')
        print('Ultra 127 never sleep til he do things right.')
        print('                                 Good luck, my friends.')



