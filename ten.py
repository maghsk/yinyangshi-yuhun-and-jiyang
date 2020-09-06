import time
import sys
if (len(sys.argv)<4):
    print(time.time()+3600*6)
else:
    h,m,s = map(int,sys.argv[1:])
    print(time.time()+3600*h+60*m+s)