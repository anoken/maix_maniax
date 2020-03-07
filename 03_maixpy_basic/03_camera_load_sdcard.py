## Copyright (c) 2019 aNoken

import sensor,image,lcd

lcd.init()
lcd.direction(lcd.YX_RLUD)

fname="test.jpg"
img_read = image.Image(fname)
lcd.display(img_read)