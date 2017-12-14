import socket
import json
import time
def receive(fd,sock):
    s = sock[fd].recv(6000)
    while 1:
        if 10 not in s:
            s = s + sock[fd].recv(6000)
        else:
            break
#    print(s.decode('ascii'))
    return s
def run(ip_and_port):
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

    filter_str1 = "int filter_function(struct User user) { return (user.age == "
    filter_str2 = " );}"
    try_match_dic = {"cmd":"try_match","name":"piepie","age":20,"gender":"male","introduction":"I am piepie~~~","filter_function":"int filter_function(struct User user) { return 1; }"}

    worst = 0.0
    total = 0.0
    count = 0
    for i in range (int(connect_num/2)):
        tmp_dic = try_match_dic
        tmp_dic["age"] = i
        tmp_dic["filter_function"] = filter_str1 + str(i) + filter_str2
        tmp_dic["name"] = "piepie" + str(i)
#        print(json.dumps(tmp_dic))
        print ("生成前一半的客戶,",int(((i+1)/(connect_num/2))*100),"%",end = '\r')
        sock[i].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        s = receive(i,sock)
    print()
    for i in range(int(connect_num/2)):
        tmp_dic = try_match_dic
        tmp_dic["age"] = int(connect_num/2)-i-1
        tmp_dic["name"] = "piepie" + str(i+int(connect_num/2))
        tmp_dic["filter_function"] = filter_str1 + str(int(connect_num/2)-i-1) + filter_str2
#        print(json.dumps(tmp_dic))
        start_time = time.time()
        sock[(connect_num-i-1)].send((json.dumps(tmp_dic)+'\n').encode('ascii'))
        s = receive((connect_num-i-1),sock)
        s = receive((connect_num-i-1),sock)
        elapsed_time = time.time() - start_time
        if elapsed_time > worst:
            worst = elapsed_time
        total = total + elapsed_time
        count = count + 1
        print ("                                                                          ",end = '\r')
        print ("Average = %fs,"%(total/count),"Worst = %fs,"%(worst),"Now = %fs"%elapsed_time,end = '\r')
    print()
    try_match = json.dumps(try_match_dic)
#    print(try_match)
#    sock[0].send((try_match+'\n').encode('ascii'))
    for i in range(connect_num):
        print ("關閉所有客戶",int(((i+1)/(connect_num))*100),"%",end = '\r')
        sock[i].close()
        time.sleep(0.2)
    print()
