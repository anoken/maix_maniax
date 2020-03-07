## Copyright (c) 2019 aNoken


import sensor,image,lcd
lcd.init()
lcd.direction(lcd.YX_RLUD)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
while True:
    img=sensor.snapshot()
    lcd.display(img)
    