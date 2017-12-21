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
    while 1:
        connect = input("客戶端數量(even)：")
        connect_num = int(connect)
        if connect_num % 2 == 1:
            print("請輸入偶數")
        else:
            break
    sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(connect_num)]
    for i in range(connect_num):
        try:
            sock[i].connect(ip_and_port)
        except:
            sock[i].close()
            print ("fd : ",i," fail.")

    filter_str1 = "int filter_function(struct User user) { int a=0; for(int i=0;i<10000000;i++){a++;} return (user.age == "
    filter_str2 = " );}"
    try_match_dic = {"cmd":"try_match","name":"piepie","age":20,"gender":"male","introduction":"I am piepie~~~","filter_function":"int filter_function(struct User user) { return 1; }"}

    worst = 0.0
    total = 0.0
    count = 0
    output = []
    timeout = 0.01
    for i in range (int(connect_num/2)):
        tmp_dic = try_match_dic
        tmp_dic["age"] = i
        tmp_dic["filter_function"] = filter_str1 + str(i) + filter_str2
        tmp_dic["name"] = "piepie" + str(i)
#        print(json.dumps(tmp_dic))
        print ("生成前一半的客戶,",int(((i+1)/(connect_num/2))*100),"%",end = '\r')
        sock[i].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        s = receive(sock[i],sock)
    print()
    for i in range(int(connect_num/2)):
        tmp_dic = try_match_dic
        tmp_dic["age"] = int(connect_num/2)-i-1
        tmp_dic["name"] = "piepie" + str(i+int(connect_num/2))
        tmp_dic["filter_function"] = filter_str1 + str(int(connect_num/2)-i-1) + filter_str2
#        print(json.dumps(tmp_dic))
        sock[int(connect_num/2)+i].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        readable, writable, exceptional = select.select(sock,output,sock,timeout);
        for fd in readable:
            tmp = receive(fd,sock)
    name = "piepie0";
    start_time = time.time()
    print(name)
    judge = 0
    start = 0
    while 1:
        readable, writable, exceptional = select.select(sock,output,sock,timeout);
        for fd in readable:
            tmp = receive(fd,sock)
            s = tmp.decode('ascii')
            print (s)
            print (name in s)
            if name in s:
                elapsed_time = time.time() - start_time
                judge = 1
        if judge == 1:
            break


    print("total = %fs"%elapsed_time)
    for i in range(connect_num):
        print ("關閉所有客戶",int(((i+1)/(connect_num))*100),"%",end = '\r')
        sock[i].close()
        time.sleep(0.2)
    print()
    print("跑跑單線ing")
    (command_output, exitstatus) = run ('time spec_two/test',withexitstatus = 1)
    time.sleep(1)
    tt = command_output.decode('ascii')
    line_time = float(tt.split('user')[0]) * (connect_num/2) * (connect_num/2+1)
    print("單線時間：",line_time)
    (command_output, exitstatus) = run ('time gcc -fPIC -shared -o spec_two/piepie0.so spec_two/piepie0.c',withexitstatus = 1)
    tt = command_output.decode('ascii')
    compile_time = float(tt.split('user')[0]) * (connect_num/2)
    print("編譯時間",compile_time)
    print("倍率 = ",(elapsed_time-compile_time)/line_time)
    return
