import socket
import json
import select
import time
import random
def receive(fd):
    s = fd.recv(6000)
    while 1:
        if 10 not in s:
            s = s + fd.recv(6000)
        else:
            break
    #print(s.decode('ascii'))
    return s
def run(ip_and_port):
    connect = input("客戶端數量：")
    print ("生成",connect,"個客戶",end = '\r')
    connect_num = int(connect)
    sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(connect_num)]
    inputs = sock
    timeout = 0.3
    outputs = []
    for i in range(connect_num):
        try:
            sock[i].connect(ip_and_port)
        except:
            sock[i].close()
            print ("fd : ",i," fail.")
    try_match_dic = {"cmd":"try_match","name":"piepie","age":20,"gender":"male","introduction":"I am piepie~~~","filter_function":"int filter_function(struct User user) { return 1; }"}
    send_dic = {"cmd": "send_message","message": "MaMa is God!","sequence": 4}
    for i in range(connect_num):
        tmp_dic = try_match_dic
        tmp_dic["name"] = "piepie" + str(i)
        print ("生成",connect,"個客戶,",int(((i+1)/(connect_num))*100),"%",end = '\r')
        sock[i].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        while 1:
            readable, writable, exceptional = select.select(inputs, outputs, inputs,timeout)
            if len(readable) == 0:
                break;
            for fd in readable:
                tmps = receive(fd)
    time.sleep(1.0)
    print()
    print("wait for 15sec patiently~~")
    count = 0
    start_time = time.time()
    times = 1
    while 1:
        for i in range(10):
            rand = random.randint(0,connect_num-1)
            sock[rand].send((json.dumps(send_dic)+'\n').encode('ascii'))
        time.sleep(0.01)
        readable, writeable, exceptional = select.select(inputs, outputs, inputs)
        for fd in readable:
            tmps = receive(fd)
            #print (tmps)
            count = count + tmps.decode('ascii').count("receive")
        if time.time() - start_time > times:
            print ("time click : ",times,",average message sent(Q/2s) : %f"%(count*2/times),",total message sent : ",count,end = '\r')
            times = times + 1
        if times > 15:
            print()
            time.sleep(1.0)
            for i in range(connect_num):
                print ("關閉所有客戶",int(((i+1)/(connect_num))*100),"%",end = '\r')
                sock[i].close()
                time.sleep(0.05)
            print()
            break

