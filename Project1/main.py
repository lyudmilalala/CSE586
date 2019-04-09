
#import
import random
import  os
import numpy
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
# from PIL import Image
import read_model

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

# RANDSAC
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

# Step5
# plot the reconstruction points with different colors for inliners and outliners
def plot3D(dic, best_para, threshold):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.view_init(30, 30)
    for k in dic:
        if getDistance(para[0],para[1],para[2],para[3],dic[k]) < threshold:
            ax.scatter3D(dic[k][0], dic[k][1], dic[k][2], c='r', s = 5)
        else:
            ax.scatter3D(dic[k][0], dic[k][1], dic[k][2], c='b', s= 5)
    fig.savefig('3Dplots.pdf')
    return fig

# Step7
# draw a 3D box
def drawBox(sidelen):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    cube_mtarix = numpy.array([[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0], [-1, -1, 2], [1, -1, 2], [1, 1, 2], [-1, 1, 2]])
    vertexes = sidelen/2*cube_mtarix
    ax.scatter3D(vertexes[:, 0], vertexes[:, 1], vertexes[:, 2], c='b', s = 5)
    ax.scatter3D(0, 0, 0, c='r', s = 5)
    edges = [[vertexes[0],vertexes[1],vertexes[2],vertexes[3]],[vertexes[4],vertexes[5],vertexes[6],vertexes[7]], [vertexes[0],vertexes[3],vertexes[7],vertexes[4]], [vertexes[1],vertexes[2],vertexes[6],vertexes[5]], [vertexes[0],vertexes[1],vertexes[5],vertexes[4]],[vertexes[2],vertexes[3],vertexes[7],vertexes[6]]]
    # faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    # faces.set_facecolor((0,0,1,0.1))
    colors = [(0.4,0.4,0.5,0.5),(0.5,0.7,1,0.5),(0.5,1,0.5,0.5),(1,0.7,0,0.5),(1,0.7,0.7,0.5),(0.6,0.4,1,0.5)]
    for i in range(6):
        f = [edges[i]]
        face = Poly3DCollection(f, linewidths=1, edgecolors='k')
        face.set_facecolor(colors[i])
        ax.add_collection3d(face)
    plt.show()
    return vertexes

# 3D to 2D with pinhole camera model
# c = (cx, cy, cz)
# vertexes = eight vertexes of the cube
def to2D(c, vetexes):
    cameras, images, points3D = read_model.read_model("/Users/jennydeng/Desktop/class/CSE586/CSE586/Project1", ".txt")
    width = cameras[1].width
    height = cameras[1].height
    focus = cameras[1].params[0]
    fpToPixel = numpy.array([[1, 0, width/2], [0, 1, height/2], [0, 0, 1]])
    translation = numpy.array([[1, 0, 0, -1*c[0]], [0, 1, 0, -1*c[1]], [0, 0, 1, -1*c[2]], [0, 0, 0, 1]])
    presectiveProjection = numpy.array([[focus, 0, 0, 0], [0, focus, 0, 0], [0, 0, 1, 0]])
    for m in images:
        plist = []
        R = qvec2rotmat(images[m].qvec)
        rotation = numpy.array([[R[0][0], R[0][1], R[0][2], 0], [R[1][0], R[1][1], R[1][2], 0], [R[2][0], R[2][1], R[2][2], 0], [0, 0, 0, 1]])
        for v in vertexes:
            worldPoint = numpy.array([[v[0]],[v[1]],[v[2]],[1]])
            pixelLoc = numpy.matmul(numpy.matmul(numpy.matmul(fpToPixel, presectiveProjection), numpy.matmul(rotation, translation)), worldPoint)
            plist.append(pixelLoc)
        draw2D(images[m].id, plist)

def draw2D(img_id, pixels):
    img = plt.imread('samples/'+str(img_id)+".jpg")
    fig, ax = plt.subplots()
    ax.imshow(img)
    bottom = Polygon(numpy.array([pixels[0],pixels[1],pixels[2],pixels[3]]), True, linewidth=1, edgecolor='k', facecolor = [0.4,0.4,0.5,1])
    ax.add_patch(bottom)
    back = Polygon(numpy.array([pixels[3],pixels[2],pixels[6],pixels[7]]), True, linewidth=1, edgecolor='k', facecolor = [0.6,0.4,1,1])
    ax.add_patch(back)
    left = Polygon(numpy.array([pixels[0],pixels[3],pixels[7],pixels[4]]), True, linewidth=1, edgecolor='k', facecolor = [1,0.7,0,1])
    ax.add_patch(left)
    top = Polygon(numpy.array([pixels[4],pixels[5],pixels[6],pixels[7]]), True, linewidth=1, edgecolor='k', facecolor = [0.2,0.4,1,0.7])
    ax.add_patch(top)
    right = Polygon(numpy.array([pixels[1],pixels[2],pixels[6],pixels[5]]), True, linewidth=1, edgecolor='k', facecolor = [0.5,1,0.5,0.7])
    ax.add_patch(right)
    front = Polygon(numpy.array([pixels[0],pixels[1],pixels[5],pixels[4]]), True, linewidth=1, edgecolor='k', facecolor = [1,0.7,0.7,0.7])
    ax.add_patch(front)
    if not os.path.exists('2Dresults'):
        os.makedirs('2Dresults')
    plt.savefig('2Dresults/'+str(img_id)+'.png')
    return 0

#************** main function ****************

#print getSpaceFunction([0,0,0],[1,0,0],[1,1,0])
#a,b,c,d = getSpaceFunction([0,0,0],[1,0,0],[1,1,0])
#print getDistance(a,b,c,d,[1,1,1])

dic = getDict()
count, para = randomChoose(dic, 0.1, 300)
print(count)
print(para)
plot3D(dic, para, 0.1)
# vlist = drawBox(1)
# to2D((0,0,0), vlist)
# draw2D(1,numpy.array([[3000,3500],[4000, 3500],[4866, 3200],[3866, 3200],[3000, 2500],[4000, 2500],[4866, 2200],[3866, 2200]]))

#end
