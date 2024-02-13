## Copyright (c) 2019 aNoken

import ulab as np
import random
import time

clock = time.clock()
a = []
b = []
for i in range(100):
    a.append(random.random())
    b.append(random.random())
print("a=",a)
print("b=",b)

c = []
for i in range(100):
    c.append(0)

#Normal Calculate Plus
start = time.ticks_us()
for i in range(100):
    c[i]=a[i]+b[i]

print("Python: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print("c=",c)

#NumPy Calculate  Plus
na = np.array(a)
nb = np.array(b)
start = time.ticks_us()
nc=na+nb
print("Numpy: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print("nc=",nc)


#Normal Calculate Diff
start = time.ticks_us()
for i in range(100):
    c[i]=a[i]-b[i]

print("Python: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print("c=",c)

#NumPy Calculate Diff
na = np.array(a)
nb = np.array(b)
start = time.ticks_us()
nc=na-nb
print("Numpy: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print("nc=",nc)

#Normal Calculate Sum
start = time.ticks_us()
sum=0
for i in range(100):
    sum+=a[i]

print("Python: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print()
print("sum=",sum)

#NumPy Calculate Sum
start = time.ticks_us()
np_sum=np.sum(a)
print("Numpy: " + str(time.ticks_diff(time.ticks_us(), start)) + " us")
print("np_sum=",np_sum)
