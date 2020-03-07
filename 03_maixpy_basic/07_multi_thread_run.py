## Copyright (c) 2019 aNoken

from Maix import GPIO
from fpioa_manager import fm
import _thread, time

lcd.init()
lcd.clear()
Lock = _thread.allocate_lock()

def testThread():
    cnt=0
    while True:
        time.sleep_ms(100)
        lcd.draw_string(0,20,"cnt1:"+str(cnt))
        cnt+=1

def testThread2():
    cnt2=0
    while True:
        time.sleep_ms(100)
        lcd.draw_string(0,50,"cnt2:"+str(cnt2))
        cnt2+=1

_thread.start_new_thread(testThread,())
_thread.start_new_thread(testThread2,())
print("done")