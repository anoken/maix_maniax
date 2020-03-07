## Copyright (c) 2019 aNoken

import video, sensor,image,lcd, time

lcd.init()
lcd.direction(lcd.YX_RLUD)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)
v = video.open("/sd/capture.avi", record=1, interval=200000, quality=50)
cnt = 0
cnt_max = 100
tim = time.ticks_ms()
while True:
    tim = time.ticks_ms()
    img = sensor.snapshot()
    lcd.display(img)
    img_len = v.record(img)
    print("record",cnt,"/",cnt_max,"time",time.ticks_ms() - tim)
    cnt += 1
    if cnt > cnt_max:
        break
print("finish")
v.record_finish()
lcd.clear()