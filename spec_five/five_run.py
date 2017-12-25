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
    connect = input("客戶端數量：")
    connect_num = int(connect)
    sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(connect_num)]
    for i in range(connect_num):
        try:
            sock[i].connect(ip_and_port)
        except:
            sock[i].close()
            print ("fd : ",i," fail.")

    filter_str1 = "int filter_function(struct User user) { int a=0; for(long long int i=0;i<200000000;i++){a+=i;} if(a == 0) puts(\"hi\"); return (user.age == "
    filter_str2 = " );}"
    try_match_dic = {"cmd":"try_match","name":"piepie","age":20,"gender":"male","introduction":"I am piepie~~~","filter_function":"int filter_function(struct User user) { return 1; }"}

    worst = 0.0
    total = 0.0
    count = 0
    output = []
    timeout = 0.01
    for i in range (connect_num):
        tmp_dic = try_match_dic
        tmp_dic["age"] = i
        tmp_dic["filter_function"] = filter_str1 + str(i) + filter_str2
        tmp_dic["name"] = "piepie" + str(i)
#        print(json.dumps(tmp_dic))
        print ("生成前一半的客戶,",int(((i+1)/(connect_num/2))*100),"%",end = '\r')
        sock[i].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        s = receive(sock[i],sock)
    print()
    for i in range(connect_num):
        print ("關閉所有客戶",int(((i+1)/(connect_num))*100),"%",end = '\r')
        sock[i].close()
        time.sleep(0.1)
    print()
    print("I send some unmatched clients to your server and close them immediately.")
    print("To check if you can support this feature, try other spec right now without closing server.")
    print("                   Good luck.")

