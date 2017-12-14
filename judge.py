#!/usr/bin/env python3
import sys
from spec_two import two_run
from spec_four import four_run
if len(sys.argv) != 3:
    print ("Please specified the host ip and port.")
    sys.exit(0)
while 1:
    check = input("1)10 人以下、篩選函式只有常數複雜度時，所有 API 回應正確\n2)以至少兩倍於單 CPU 的速度處理篩選函式\n3)能抵擋惡意篩選函式，不使伺服器停擺\n4)支援 1000 人上線、兩秒內 100 條訊息傳遞（無論篩選函式的忙碌程度)\n")
    if 0 < int(check) < 5:
        if int(check) == 2:
            two_run.run((str(sys.argv[1]),int(sys.argv[2])))
        if int(check) == 4:
            four_run.run((str(sys.argv[1]),int(sys.argv[2])))
        break
