## Copyright (c) 2019 aNoken

import sensor, image, lcd, time
import KPU as kpu
lcd.init()
lcd.rotation(2)
lcd.clear()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)
labels = ['001_class', '002_class', '003_class', '004_class']
task = kpu.load("my_mbnet.kmodel")
clock = time.clock()
while(True):
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    a = lcd.display(img)
    lcd.draw_string(10, 96, "%.2f:%s"%(pmax, labels[max_index].strip()))
    print(fps)
a = kpu.deinit(task)

