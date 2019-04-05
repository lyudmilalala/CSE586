
#import
import random
import  os
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#retrive the dictionary
def getDict():
    dic = {}
    with open("points3D.txt","r") as n:
        for i, line in enumerate(n):
            if i>2:
                a = line.split(" ")
                temp = []
                temp.append(float(a[1]))
                temp.append(float(a[2]))
                temp.append(float(a[3]))
                dic[int(a[0])] = temp[:]
    return dic

#get the plane function by three point
def getSpaceFunction(p1,p2,p3):
    a = ((p2[1] - p1[1]) * (p3[2] - p1[2]) - (p2[2] - p1[2]) * (p3[1] - p1[1]))
    b = ((p2[2] - p1[2]) * (p3[0] - p1[0]) - (p2[0] - p1[0]) * (p3[2] - p1[2]))
    c = ((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]))
    d = (0 - (a * p1[0] + b * p1[1] + c * p1[2]))
    return a,b,c,d

#get the distance between a point and a plance
def getDistance(a,b,c,d,p): #ax+by+cz+d, where p is the point
    up = abs(a*p[0]+b*p[1]+c*p[2]+d)
    down = (a*a+b*b+c*c)**0.5
    return up/down

#count how many point are statisfied the rule that the distance should be less than threshold
def evaluatePlane(a,b,c,d,threshold,dic):
    count = 0
    for point in list(dic.values()):
        if getDistance(a,b,c,d,point) < threshold:
            count += 1
    return count

def randomChoose(dic, threshold, iter): #threshold is the allowable distance between points and plane
    maxCount = 0
    dlist = list(dic.values())#dict values
    bestParam = [] # a,b,c,d
    for i in range(iter):
        p1 = random.randint(1, len(dic)) #choose three points, get the index
        p2 = random.randint(1, len(dic))
        p3 = random.randint(1, len(dic))
        a,b,c,d = getSpaceFunction(dlist[p1], dlist[p2], dlist[p3])# get plane function
        thisCount = evaluatePlane(a,b,c,d,threshold,dic) #count the number of good points
        if thisCount > maxCount:
            maxCount = thisCount
            bestParam = [a,b,c,d]
    return maxCount,bestParam

def plot3D(dic, best_para, threshold):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    for k in dic:
        if getDistance(para[0],para[1],para[2],para[3],dic[k]) < threshold:
            ax.scatter(dic[k][0], dic[k][1], dic[k][2], c='r', s = 5)
        else:
            ax.scatter(dic[k][0], dic[k][1], dic[k][2], c='b', s= 5)
    fig.savefig('3Dplots.pdf')

#************** main function ****************

#print getSpaceFunction([0,0,0],[1,0,0],[1,1,0])
#a,b,c,d = getSpaceFunction([0,0,0],[1,0,0],[1,1,0])
#print getDistance(a,b,c,d,[1,1,1])
dic = getDict()
count, para = randomChoose(dic, 0.1, 3000)
print(count)
print(para)
plot3D(dic, para, 0.1)
#end
