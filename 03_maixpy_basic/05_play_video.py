## Copyright (c) 2019 aNoken

import video,time,lcd

lcd.init()
lcd.direction(lcd.YX_RLUD)

v = video.open("/sd/capture.avi")
print(v)
v.volume(50)
while True:
    if v.play() == 0:
        print("play end")
        break
v.__del__()
