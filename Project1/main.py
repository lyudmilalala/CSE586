
#import
import random
import  os
import numpy


dic = {}
with open("points3D.txt","r") as n:
    for line in n:
        a = line.split(" ")
        temp = []
        temp.append(float(a[1]))
        temp.append(float(a[2]))
        temp.append(float(a[3]))
        dic[a[0]] = temp[:]
print(dic["1"])






























#end
