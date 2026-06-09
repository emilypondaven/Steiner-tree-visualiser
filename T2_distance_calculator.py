import matplotlib.pyplot as plt
import matplotlib.animation as ani
from shapely.geometry import Polygon
from matplotlib.widgets import Button
import numpy as np
import math
from skspatial.objects import Circle
from skspatial.objects import Line
from skspatial.plotting import plot_2d

def maths_points_calculator(p, d, angle, size):
    # p=previous point coordinate
    # d=distance to previous point
    # angle=angle with sin()
    # size='True' if this point is bigger than previous, 'False' if this point is smaller than previous
    if size==True:
        return p+d*math.sin(angle/180*math.pi)
    
    if size==False:
        return p-d*math.sin(angle/180*math.pi)

def calculate_initialPOINTS(x1,y1,s):
    # point A
    x1,y1=x1,y1

    # point B
    angle1 = initial_angle
    angle2 = 90-angle1
    length = pointA_pointB*s
    x2, y2 = maths_points_calculator(x1,length,angle2,True), maths_points_calculator(y1,length,angle1,True)

    # point C
    angle1 = angle_ABC-angle2
    angle2 = 90-angle1
    length = pointB_pointC*s
    x3, y3 = maths_points_calculator(x2,length,angle1,True), maths_points_calculator(y2,length,angle2,False)

    # point D
    angle1 = angle_BCD-angle2
    angle2 = 90-angle1
    length = pointC_pointD*s
    x4, y4 = maths_points_calculator(x3,length,angle2,False), maths_points_calculator(y3,length,angle1,False)

    x_values=np.array([x1,x2,x3,x4])
    y_values=np.array([y1,y2,y3,y4])


    return [x_values,y_values]

def ABCDnames_STEP0(x,y):
    t1=main_fig.text(x[0]-15, y[0]+0.25, "A")
    t2=main_fig.text(x[1]+3, y[1]-0.25, "B")
    t3=main_fig.text(x[2]+3, y[2]+0.25, "C")
    t4=main_fig.text(x[3]+3, y[3]-0.25, "D")

    return [t1,t2,t3,t4]

def draw_line(a,b):
    return main_fig.plot([a[0],b[0]], [a[1],b[1]],c='blue',linewidth=.5)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def calculate_distance(x1,y1,x2,y2):
    # using cosine rule
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return d


#INITIAL VARIABLES
GREY = (0.78, 0.78, 0.78)
RED = (0.96, 0.15, 0.15) 
GREEN = (0, 0.86, 0.03)    
BLACK = (0, 0, 0) 

point_size=20
height, width = 517,1200



main_fig = plt.subplot(111)
plt.subplots_adjust(bottom=0.2)
main_fig.set_ylim([0, height])
main_fig.set_xlim([0, width])

# GENERAL VARIABLES

# distance
pointA_pointB=104
pointB_pointC=97
pointC_pointD=73
pointD_pointA=126

# angle between points
initial_angle=24
angle_DAB=81
angle_ABC=80
angle_BCD=119
angle_CDA=80


# MAIN CODE

list_initialpoints = calculate_initialPOINTS(width/3,2*height/3,3) 
x_initial = list_initialpoints[0]
y_initial = list_initialpoints[1]

# paste points on screen
all_points0 = [main_fig.scatter(x_initial, y_initial, s=10, c="blue")]
all_text0 = ABCDnames_STEP0(x_initial,y_initial)
lineAC=draw_line([x_initial[0],y_initial[0]],[x_initial[2],y_initial[2]])
lineBD=draw_line([x_initial[1],y_initial[1]],[x_initial[3],y_initial[3]])

# find slope of each line
mAC=(y_initial[0]-y_initial[2])/(x_initial[0]-x_initial[2])
mBD=(y_initial[1]-y_initial[3])/(x_initial[1]-x_initial[3])
cAC=y_initial[0]-mAC*x_initial[0]
cBD=y_initial[1]-mBD*x_initial[1]
x_intersect=(cBD-cAC)/(mAC-mBD)
y_intersect=mAC*x_intersect+cAC
point_intersect = main_fig.scatter(x_intersect, y_intersect, s=point_size, c="green")
text=main_fig.text(x_intersect+5, y_intersect, "P")

# calculate total_distance
dist_AP=calculate_distance(x_initial[0],y_initial[0],x_intersect,y_intersect)/3
dist_BP=calculate_distance(x_initial[1],y_initial[1],x_intersect,y_intersect)/3
dist_CP=calculate_distance(x_initial[2],y_initial[2],x_intersect,y_intersect)/3
dist_DP=calculate_distance(x_initial[3],y_initial[3],x_intersect,y_intersect)/3
print(dist_AP, dist_BP, dist_CP, dist_DP)
total_distance=dist_AP+ dist_BP+ dist_CP+ dist_DP
main_fig.text(900,50,"Total distance = "+str(round(total_distance,2)))


# Show the plot after running through code
plt.show()
