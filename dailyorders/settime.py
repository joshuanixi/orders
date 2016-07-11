#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sched, time
from threading import Thread, Timer
import subprocess




schedule = sched.scheduler ( time.time, time.sleep )  
  
def func(string1,float1):  
    print ("now is",time.time()," | output=",string1,float1 )
  
print (time.time()  )
schedule.enter(2,0,func,("test1",time.time()))  
schedule.enter(2,0,func,("test1",time.time()))  
schedule.enter(3,0,func,("test1",time.time()))  
schedule.enter(4,0,func,("test1",time.time()))  
schedule.run()  
print (time.time() ) 





'''

s = sched.scheduler(time.time, time.sleep)

class Job(Thread):
    def run(self):
        #主要业务执行方法
        print_time()
        print ("-------------- compiling --------------")
        subprocess.Popen("compile.sh", cwd="/bes/nj-build")

def each_day_time(hour,min,sec,next_day=True):
    #返回当天指定时分秒的时间
    struct = time.localtime()

    if next_day:
        day = struct.tm_mday + 1
    else:
        day = struct.tm_mday
    return time.mktime((struct.tm_year,struct.tm_mon,day,
        hour,min,sec,struct.tm_wday, struct.tm_yday,
        struct.tm_isdst))
    
def print_time(name="None"):
    print (name, ":","From print_time",\
        time.time()," :", time.ctime())

def do_somthing():
    job = Job()
    job.start()

def echo_start_msg():
    print ("-------------- auto compile begin running --------------")

def main():
    print(time.localtime())
    print(each_day_time(0,0,0,True))
    #指定时间点执行任务
    #s.enterabs(each_day_time(14,45,0,True), 1, echo_start_msg, ())
    s.run()
    while(True):
        Timer(0, do_somthing, ()).start()
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()
'''