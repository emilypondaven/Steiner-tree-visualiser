import matplotlib.pyplot as plt
import matplotlib.animation as ani
from shapely.geometry import Polygon
from matplotlib.widgets import Button
import numpy as np
import math
from skspatial.objects import Circle
from skspatial.objects import Line
from skspatial.plotting import plot_2d

plt.rcParams.update({'font.size': 15})

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

    if steiner_tree == '1':
        x_values=np.array([x1,x2,x3,x4])
        y_values=np.array([y1,y2,y3,y4])

    if steiner_tree == '2':
        x_values=np.array([x2,x3,x4,x1])
        y_values=np.array([y2,y3,y4,y1])

    return [x_values,y_values]

def e_point(a1,b1, a2, b2, d,ang,sign):
    extra1 = [maths_points_calculator(a1[0], d, 90-60, True), maths_points_calculator(a1[1], d, 60, True)]

    # Rotation of by angle specified
    extra1[0]-=a1[0]
    extra1[1]-=a1[1]
    extra1[1]=d*math.sin((ang)/180*math.pi)*sign[0]
    extra1[0]=d*math.cos((ang)/180*math.pi)*sign[1]
    #e1[0]=e1[0]*math.cos(24/180*math.pi)-e1[1]*math.sin(24/180*math.pi)
    #e1[1]=e1[1]*math.cos(24/180*math.pi)+e1[0]*math.sin(24/180*math.pi)
    extra1[0]+=a1[0]
    extra1[1]+=a1[1]

    extra2=e_point_reflection(a1,b1,extra1)     # find point e2 which is reflection of e1
    extra2[0]=extra2[0]+(a2[0]-a1[0])

    # rename extra points
    extra1_coor = extra1
    extra2_coor = extra2
    extra1 = main_fig.scatter(extra1[0], extra1[1], s=point_size, c="green")
    extra2 = main_fig.scatter(extra2[0], extra2[1], s=point_size, c="green")

    return extra1,extra2, extra1_coor, extra2_coor

def e_point_reflection(a,b,e):
    e2=[0,0]
    middle_point=[0,0]
    m=(a[1]-b[1])/(a[0]-b[0])
    mN=-1/m
    middle_point[0]=(m*a[0]-mN*e[0]+e[1]-a[1])/(m-mN)
    middle_point[1]=m*(middle_point[0]-a[0])+a[1]
    e2[0]=middle_point[0]*2-e[0]
    e2[1]=middle_point[1]*2-e[1]

    return e2

def draw_triangle(a,b,e):
    #line segments
    line1 = main_fig.plot([a[0],b[0]], [a[1],b[1]],c='blue',linewidth=.5)
    line2= main_fig.plot([a[0],e[0]], [a[1],e[1]],c='blue',linewidth=.5)
    line3 = main_fig.plot([e[0],b[0]], [e[1],b[1]],c='blue',linewidth=.5)

    tri=[line1[0],line2[0],line3[0]]
    return tri

def draw_circle(c,r):
    circle1 = plt.Circle((c[0], c[1]), r, color='blue', fill=False)
    circle1 = main_fig.add_patch(circle1)

    return circle1

def draw_line(a,b):
    return main_fig.plot([a[0],b[0]], [a[1],b[1]],c='blue',linewidth=.5)

def center_triangle(a,b,c):
    centerX = (a[0] + b[0] + c[0]) / 3
    centerY = (a[1] + b[1] + c[1]) / 3
    return [centerX,centerY]

def calculate_distance(x1,y1,x2,y2):
    # using cosine rule
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return d

def find_angle_rotation(y1,y2,d):
    an = (math.asin(abs(y1-y2)/d))/math.pi*180
    if y1<y2:
        return an+60
    else:
        return 60-an

def triangle_drawing_steps(start1, finish1, start2, finish2, sign,t):
    length=calculate_distance(start1[0],start1[1],finish1[0],finish1[1])     #distance of line e1 to c
    theta=find_angle_rotation(start1[1],finish1[1],length)     # ANGLE OF ROTATION
    extra1,extra2,extra1_coor,extra2_coor = e_point(start1,finish1, start2, finish2, length,theta, sign)     # calculate extra points e5 and e6

    # draw triangle
    if t:
        triE1=draw_triangle(start1,finish1,extra1_coor)
        triE2=draw_triangle(start2,finish2,extra2_coor)
    else:
        triE1=0
        triE2=0
    
    return extra1,extra2,extra1_coor, extra2_coor, triE1, triE2

def remove(p,t,s):
    # p=points
    # t=texts
    # s=line_segment
    all_elements=p+t+s
    for element in all_elements:
        element.remove()

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def shortest_distance(A,B1,B2):
    dis_1=math.sqrt((A[0]-B1[0])**2+(A[1]-B1[1])**2)
    dis_2=math.sqrt((A[0]-B2[0])**2+(A[1]-B2[1])**2)
    if dis_1<dis_2:
        return B2
    else:
        return B1

def Heinens_Method(a,b,c,d,show,lst):
    center = center_triangle(a,b,c)
    radius = calculate_distance(a[0],a[1],center[0],center[1])
    if show:
        lst.append(draw_circle(center,radius))

        lst.append(draw_line(b,d))

    # using scikit-spatial library
    circle=Circle(center,radius)
    line=Line(b,[d[0]-b[0],d[1]-b[1]])
    point_a,point_b=circle.intersect_line(line)
    steiner_coor=shortest_distance(b,point_a,point_b)
    if show: 
        steiner_point=main_fig.scatter(steiner_coor[0], steiner_coor[1], s=20, c="orange")
    else:
        steiner_point=0
    if steiner_coor[0] > a[0] and steiner_coor[0] < c[0]:
    # draw lines connecting to steiner point
        if show:
            line1=draw_line(b,steiner_coor)
            line2=draw_line(c,steiner_coor)
            line3=draw_line(a,steiner_coor)
        else:
            line1,line2,line3=0,0,0
    else:
        line1,line2,line3=0,0,0

    return line1,line2,line3,steiner_point, steiner_coor,lst


# TEXT ANNOTATIONS NEXT TO POINTS
def ABCDnames_STEP0(x,y):
    t1=main_fig.text(x[0]-20, y[0]+0.25, "A")
    t2=main_fig.text(x[1]+3, y[1]-0.25, "B")
    t3=main_fig.text(x[2]+3, y[2]+0.25, "C")
    t4=main_fig.text(x[3]+5, y[3]-0.25, "D")

    return [t1,t2,t3,t4]

def ABCDnames_STEP2(x,y,e1_c,e2_c):
    t1=main_fig.text(x[2]+5, y[2]-2, "C")
    t2=main_fig.text(x[3]+8, y[3]-10, "D")
    if e1_c!=0:
        e1=main_fig.text(e1_c[0]-25, e1_c[1]+3, "E₁")
        return [t1,t2,e1]
    if e2_c!=0:
        e2=main_fig.text(e2_c[0]-25, e2_c[1]+0.25, "E₂")
        return [t1,t2,e2]


#INITIAL VARIABLES
GREY = (0.78, 0.78, 0.78)
RED = (0.96, 0.15, 0.15) 
GREEN = (0, 0.86, 0.03)    
BLACK = (0, 0, 0) 

point_size=20
height, width = 517,1200

class Shape():
    def step_0(self, event):
        global all_points0, all_text0
        # initial points A,B,C,D
        list_initialpoints = calculate_initialPOINTS(width/3,2*height/3,3) 
        x_initial = list_initialpoints[0]
        y_initial = list_initialpoints[1]

        # paste points on screen
        all_points0 = [main_fig.scatter(x_initial, y_initial, s=10, c="blue")]
        all_text0 = ABCDnames_STEP0(x_initial,y_initial)

    def step_1(self,event):
        global all_points1,all_text1,all_shapes1
        
        # Remove all previous elements from step 0
        remove(all_points0, all_text0,[])

        # Insert A,B,C,D points and paste on screen
        list_initialpoints_1=calculate_initialPOINTS(width/5,height/2,2) 
        list_initialpoints_2=calculate_initialPOINTS(3*width/5,height/2,2) 

        S1x_initial_1, S1x_initial_2 = list_initialpoints_1[0], list_initialpoints_2[0]
        S1y_initial_1, S1y_initial_2 = list_initialpoints_1[1], list_initialpoints_2[1]

        S1all_points_1 = main_fig.scatter(S1x_initial_1, S1y_initial_1, s=10, c="blue")
        S1all_points_2 = main_fig.scatter(S1x_initial_2, S1y_initial_2, s=10, c="blue")

        S1all_text_1=ABCDnames_STEP0(S1x_initial_1, S1y_initial_1)
        S1all_text_2=ABCDnames_STEP0(S1x_initial_2, S1y_initial_2)


        # TRIANGLE A TO B
        e1,e2,e1_coor,e2_coor,abe1,abe2 = triangle_drawing_steps([S1x_initial_1[0],S1y_initial_1[0]], [S1x_initial_1[1],S1y_initial_1[1]], [S1x_initial_2[0],S1y_initial_2[0]], [S1x_initial_2[1],S1y_initial_2[1]],[1,1],True)
        txtE1 = main_fig.text(e1_coor[0]-13, e1_coor[1]+5, "E₁") #subscript: https://stackoverflow.com/questions/24391892/printing-subscript-in-python
        txtE2 = main_fig.text(e2_coor[0]+3, e2_coor[1]-8, "E₂")

        # Collect all required points/text/segments into given list
        all_points1=[S1all_points_1,S1all_points_2,e1,e2]
        all_text1=S1all_text_1+S1all_text_2+[txtE1,txtE2]
        all_shapes1=abe1+abe2

    def step_2(self,event):
        global all_points2,all_text2,all_shapes2
        #INITIAL GLOBALISING VARIABLES
        global S2e3_coor_1,S2e4_coor_2, S2e3_coor_3,S2e4_coor_4
        global S2e1_coor_1, S2x_initial_1, S2y_initial_1
        global S2e1_coor_2, S2x_initial_2, S2y_initial_2
        global S2e2_coor_3, S2x_initial_3, S2y_initial_3
        global S2e2_coor_4, S2x_initial_4, S2y_initial_4

        # Remove all previous elements from step 0
        remove(all_points1,all_text1,all_shapes1)


        # Insert E₁E₂CD points and paste on screen
        list_initialpoints_1=calculate_initialPOINTS(0.5*width/5,height/2,1)
        list_initialpoints_2=calculate_initialPOINTS(2*width/5,height/2,1)
        list_initialpoints_3=calculate_initialPOINTS(3*width/5,height/2,1)
        list_initialpoints_4=calculate_initialPOINTS(4*width/5,height/2,1)

        S2x_initial_1, S2x_initial_2, S2x_initial_3, S2x_initial_4 = list_initialpoints_1[0], list_initialpoints_2[0], list_initialpoints_3[0], list_initialpoints_4[0]
        S2y_initial_1, S2y_initial_2, S2y_initial_3, S2y_initial_4 = list_initialpoints_1[1], list_initialpoints_2[1], list_initialpoints_3[1], list_initialpoints_4[1]

        S2all_points_1 = main_fig.scatter(S2x_initial_1[2:], S2y_initial_1[2:], s=10, c="blue")
        S2all_points_2 = main_fig.scatter(S2x_initial_2[2:], S2y_initial_2[2:], s=10, c="blue")
        S2all_points_3 = main_fig.scatter(S2x_initial_3[2:], S2y_initial_3[2:], s=10, c="blue")
        S2all_points_4 = main_fig.scatter(S2x_initial_4[2:], S2y_initial_4[2:], s=10, c="blue")


        S2e1_1,S2e2_1,S2e1_coor_1,S2e2_coor_1,x,x = triangle_drawing_steps([S2x_initial_1[0],S2y_initial_1[0]], [S2x_initial_1[1],S2y_initial_1[1]], [S2x_initial_1[0],S2y_initial_1[0]], [S2x_initial_1[1],S2y_initial_1[1]],[1,1],False)
        S2e1_2,S2e2_2,S2e1_coor_2,S2e2_coor_2,x,x = triangle_drawing_steps([S2x_initial_2[0],S2y_initial_2[0]], [S2x_initial_2[1],S2y_initial_2[1]], [S2x_initial_2[0],S2y_initial_2[0]], [S2x_initial_2[1],S2y_initial_2[1]],[1,1],False)
        S2e2_1.remove()
        S2e2_2.remove()
        S2e1_3,S2e2_3,S2e1_coor_3,S2e2_coor_3,x,x = triangle_drawing_steps([S2x_initial_3[0],S2y_initial_3[0]], [S2x_initial_3[1],S2y_initial_3[1]], [S2x_initial_3[0],S2y_initial_3[0]], [S2x_initial_3[1],S2y_initial_3[1]],[1,1],False)
        S2e1_4,S2e2_4,S2e1_coor_4,S2e2_coor_4,x,x = triangle_drawing_steps([S2x_initial_4[0],S2y_initial_4[0]], [S2x_initial_4[1],S2y_initial_4[1]], [S2x_initial_4[0],S2y_initial_4[0]], [S2x_initial_4[1],S2y_initial_4[1]],[1,1],False)
        S2e1_3.remove()
        S2e1_4.remove()

        S2all_text_1=ABCDnames_STEP2(S2x_initial_1, S2y_initial_1,S2e1_coor_1,0)
        S2all_text_2=ABCDnames_STEP2(S2x_initial_2, S2y_initial_2,S2e1_coor_2,0)
        S2all_text_3=ABCDnames_STEP2(S2x_initial_3, S2y_initial_3,0,S2e2_coor_3)
        S2all_text_4=ABCDnames_STEP2(S2x_initial_4, S2y_initial_4,0,S2e2_coor_4)

        # TRIANGLE E1 TO C
        if steiner_tree=='1':
            S2e3_1,S2e4_2,S2e3_coor_1,S2e4_coor_2,e1ce3,e1ce4 = triangle_drawing_steps(S2e1_coor_1, [S2x_initial_1[2],S2y_initial_1[2]], S2e1_coor_2, [S2x_initial_2[2],S2y_initial_2[2]],[1,1],True)
        
        if steiner_tree=='2':
            S2e3_1,S2e4_2,S2e3_coor_1,S2e4_coor_2,e1ce3,e1ce4 = triangle_drawing_steps(S2e1_coor_1, [S2x_initial_1[2],S2y_initial_1[2]], S2e1_coor_2, [S2x_initial_2[2],S2y_initial_2[2]],[1,-1],True)
            
        S2e3_3,S2e4_4,S2e3_coor_3,S2e4_coor_4,e2ce3,e2ce4 = triangle_drawing_steps(S2e2_coor_3, [S2x_initial_3[2],S2y_initial_3[2]], S2e2_coor_4, [S2x_initial_4[2],S2y_initial_4[2]],[1,1],True)
        
        txtE3_1 = main_fig.text(S2e3_coor_1[0]-10, S2e3_coor_1[1]+5, "E₃")
        txtE4_2 = main_fig.text(S2e4_coor_2[0]+3, S2e4_coor_2[1]-20, "E₄")
        txtE3_3 = main_fig.text(S2e3_coor_3[0]-10, S2e3_coor_3[1]+5, "E₃")
        txtE4_4 = main_fig.text(S2e4_coor_4[0]+5, S2e4_coor_4[1]-0.25, "E₄")

        # Collect all required points/text/segments into given list
        all_points2=[S2all_points_1,S2all_points_2,S2all_points_3,S2all_points_4, S2e1_1,S2e1_2,S2e2_3,S2e2_4,S2e3_1,S2e4_2,S2e3_3,S2e4_4]
        all_text2=S2all_text_1+S2all_text_2+S2all_text_3+S2all_text_4+[txtE3_1,txtE4_2,txtE3_3,txtE4_4]
        all_shapes2=e1ce3+e1ce4+e2ce3+e2ce4 

    def step_3(self,event):
        global all_points3, all_text3, all_shapes3, correct_diagrams

        # create triangles and lines in preparation to be drawn
        all_ecd_triangles=[[(S2e1_coor_1[0],S2e1_coor_1[1]),(S2x_initial_1[2],S2y_initial_1[2]),(S2x_initial_1[3],S2y_initial_1[3])],
                    [(S2e1_coor_2[0],S2e1_coor_2[1]),(S2x_initial_2[2],S2y_initial_1[2]),(S2x_initial_2[3],S2y_initial_2[3])],
                    [(S2e2_coor_3[0],S2e2_coor_3[1]),(S2x_initial_3[2],S2y_initial_2[2]),(S2x_initial_3[3],S2y_initial_3[3])],
                    [(S2e2_coor_4[0],S2e2_coor_4[1]),(S2x_initial_4[2],S2y_initial_3[2]),(S2x_initial_4[3],S2y_initial_4[3])]]

        all_eec_triangles=[[(S2e1_coor_1[0],S2e1_coor_1[1]),(S2x_initial_1[2],S2y_initial_1[2]),(S2e3_coor_1[0],S2e3_coor_1[1])],
                    [(S2e1_coor_2[0],S2e1_coor_2[1]),(S2x_initial_2[2],S2y_initial_1[2]),(S2e4_coor_2[0],S2e4_coor_2[1])],
                    [(S2e2_coor_3[0],S2e2_coor_3[1]),(S2x_initial_3[2],S2y_initial_2[2]),(S2e3_coor_3[0],S2e3_coor_3[1])],
                    [(S2e2_coor_4[0],S2e2_coor_4[1]),(S2x_initial_4[2],S2y_initial_3[2]),(S2e4_coor_4[0],S2e4_coor_4[1])]]
        
        simpson_line = [[S2e1_coor_1,[S2x_initial_1[3],S2y_initial_1[3]]],
                    [S2e1_coor_2,[S2x_initial_2[3],S2y_initial_2[3]]],
                    [[S2x_initial_3[2],S2y_initial_3[2]],[S2x_initial_3[3],S2y_initial_3[3]]],
                    [[S2x_initial_4[2],S2y_initial_4[2]],[S2x_initial_4[3],S2y_initial_4[3]]]]
        
        line_intersect_checker = [[S2e1_coor_1,[S2x_initial_1[3],S2y_initial_1[3]],S2e1_coor_1,[S2x_initial_1[2],S2y_initial_1[2]]],
                    [S2e1_coor_2,[S2x_initial_2[3],S2y_initial_2[3]],S2e4_coor_2,[S2x_initial_2[2],S2y_initial_2[2]]],
                    [[S2x_initial_3[2],S2y_initial_3[2]],[S2x_initial_3[3],S2y_initial_3[3]],S2e2_coor_3,[S2x_initial_3[2],S2y_initial_3[2]]],
                    [[S2x_initial_4[2],S2y_initial_4[2]],[S2x_initial_4[3],S2y_initial_4[3]],S2e2_coor_4, S2e4_coor_4]]
        c = ['green', 'yellow']
        triangle_list=[]
        line_list=[]
        # Paste triangles on screen
        for trian in all_ecd_triangles: 
            trian = plt.Polygon(trian, color='green', alpha=0.4)
            trian = main_fig.add_patch(trian) # draw triangle
            triangle_list.append(trian)
        for trian in all_eec_triangles: 
            trian = plt.Polygon(trian, color='yellow', alpha=0.4)
            trian = main_fig.add_patch(trian) # draw triangle
            triangle_list.append(trian)
        
        # Paste lines on screen
        for line in simpson_line:
            line_list.append(draw_line(line[0],line[1])[0])

        correct_diagrams = []
        # Check if two lines intersect (using line segment intersection algorithm)
        for lines in line_intersect_checker:
            checker = intersect(lines[0],lines[1],lines[2],lines[3])
            if checker==False:
                correct_diagrams.append(line_intersect_checker.index(lines))
        
        # Collect all required points/text/segments into given list
        all_points3=all_points2
        all_text3=all_text2
        all_shapes3=all_shapes2+triangle_list+line_list

    def step_4_1(self,event):
        global heinens_method_shapes_1, all_points4_1, all_text4_1, all_shapes4_1
        heinens_method_shapes_1=[]

        # Remove all previous elements from step 3
        remove(all_points3,all_text3,all_shapes3)

        S4list_initialpoints_1=calculate_initialPOINTS(width/5,height/2,1)
        S4list_initialpoints_2=calculate_initialPOINTS(width/2,height/2,1)
        S4list_initialpoints_3=calculate_initialPOINTS(75*width/100,height/2,1)

        S4x_initial_1, S4x_initial_2, S4x_initial_3 = S4list_initialpoints_1[0], S4list_initialpoints_2[0], S4list_initialpoints_3[0]
        S4y_initial_1, S4y_initial_2, S4y_initial_3 = S4list_initialpoints_1[1], S4list_initialpoints_2[1], S4list_initialpoints_3[1]

        S4all_points_1 = main_fig.scatter(S4x_initial_1[2:], S4y_initial_1[2:], s=10, c="blue")
        S4all_points_2 = main_fig.scatter(S4x_initial_2, S4y_initial_2, s=10, c="blue")
        S4all_points_3 = main_fig.scatter(S4x_initial_3, S4y_initial_3, s=10, c="blue")

        # Heinen's method shapes
        heinens_method_shapes=[]
        # DRAW DIAGRAM 1
        S4e1_1,S4e2_1,S4e1_coor_1,S4e2_coor_1,x,x = triangle_drawing_steps([S4x_initial_1[0],S4y_initial_1[0]], [S4x_initial_1[1],S4y_initial_1[1]], [S4x_initial_1[0],S4y_initial_1[0]], [S4x_initial_1[1],S4y_initial_1[1]],[1,1],False)
        S4e2_1.remove()
        if steiner_tree=='1':
            S4e3_1,S4e4_1,S4e3_coor_1,S4e4_coor_1,e1ce3,e1ce4 = triangle_drawing_steps(S4e1_coor_1, [S4x_initial_1[2],S4y_initial_1[2]], S4e1_coor_1, [S4x_initial_1[2],S4y_initial_1[2]],[1,1],True)
            S4e4_1.remove()
            for line in e1ce4:
                line.remove()
        elif steiner_tree=='2':
            S4e3_1,S4e4_1,S4e3_coor_1,S4e4_coor_1,e1ce3,e1ce4 = triangle_drawing_steps(S4e1_coor_1, [S4x_initial_1[2],S4y_initial_1[2]], S4e1_coor_1, [S4x_initial_1[2],S4y_initial_1[2]],[1,-1],True)
            S4e3_1.remove()
            for line in e1ce3:
                line.remove()

            S4e3_1=S4e4_1
            e1ce3=e1ce4
            S4e3_coor_1=S4e4_coor_1


        
        s1d_1,s1c_1,s1e1_1,steiner1_1, steiner1_coor_1,heinens_method_shapes_1 = Heinens_Method(S4e1_coor_1,S4e3_coor_1, [S4x_initial_1[2],S4y_initial_1[2]], [S4x_initial_1[3],S4y_initial_1[3]], True, heinens_method_shapes_1)

        #text
        txt1_1 = main_fig.text(S4x_initial_1[3]-18, S4y_initial_1[3]+0.25, "D")
        txt2_1 = main_fig.text(S4x_initial_1[2]+3, S4y_initial_1[2]-18, "C")
        txt3_1 = main_fig.text(S4e1_coor_1[0]-25, S4e1_coor_1[1]+0.25, "E₁")
        txt4_1 = main_fig.text(S4e3_coor_1[0]+5, S4e3_coor_1[1]-0.25, "E₃")
        txt5_1 = main_fig.text(steiner1_coor_1[0]-30, steiner1_coor_1[1]-15, "S₁")
        all_text=[txt1_1,txt2_1,txt3_1,txt4_1,txt5_1]

        # DRAW DIAGRAM 2
        S4e1_2,S4e2_2,S4e1_coor_2,S4e2_coor_2,abe1,abe2 = triangle_drawing_steps([S4x_initial_2[0],S4y_initial_2[0]], [S4x_initial_2[1],S4y_initial_2[1]],[S4x_initial_2[0],S4y_initial_2[0]], [S4x_initial_2[1],S4y_initial_2[1]],[1,1],True)
        S4e2_2.remove()
        for line in abe2:
            line.remove()
        
        dis_1_2 = S4x_initial_2[3]-S4x_initial_1[3]

        steiner1_coor_2=[steiner1_coor_1[0]+dis_1_2,steiner1_coor_1[1]]
        steiner1_2 = main_fig.scatter(steiner1_coor_2[0], steiner1_coor_2[1], s=20, c="orange")
        s1d_2=draw_line([S4x_initial_2[2],S4y_initial_2[2]],steiner1_coor_2)
        s1c_2=draw_line([S4x_initial_2[3],S4y_initial_2[3]],steiner1_coor_2)
        s1e1_2=draw_line(steiner1_coor_2,S4e1_coor_2)

        s2s1,s2b,s2c,steiner2_2, steiner2_coor_2, heinens_method_shapes_1 = Heinens_Method([S4x_initial_2[0],S4y_initial_2[0]],S4e1_coor_2, [S4x_initial_2[1],S4y_initial_2[1]], steiner1_coor_2, True,heinens_method_shapes_1)

        #text
        txt1_2 = main_fig.text(S4x_initial_2[3]-18, S4y_initial_2[3]+0.25, "D")
        txt2_2 = main_fig.text(S4x_initial_2[2]+5, S4y_initial_2[2]-0.25, "C")
        txt3_2 = main_fig.text(S4e1_coor_2[0]-9, S4e1_coor_2[1]+7, "E₁")
        txt4_2 = main_fig.text(steiner2_coor_2[0]+10, steiner2_coor_2[1]-10, "S₂")
        txt5_2 = main_fig.text(steiner1_coor_2[0]-27, steiner1_coor_2[1]-2, "S₁")
        txt6_2 = main_fig.text(S4x_initial_2[0]-19, S4y_initial_2[0]-10, "A")
        txt7_2 = main_fig.text(S4x_initial_2[1]+5, S4y_initial_2[1]+0.25, "B")
        all_text+=[txt1_2,txt2_2,txt3_2,txt4_2,txt5_2,txt6_2,txt7_2]


        # DRAW DIAGRAM 3
        dis_2_3 = S4x_initial_3[3]-S4x_initial_2[3]

        steiner1_coor_3, steiner2_coor_3=[steiner1_coor_2[0]+dis_2_3,steiner1_coor_2[1]], [steiner2_coor_2[0]+dis_2_3,steiner2_coor_2[1]]
        steiner1_3=main_fig.scatter(steiner1_coor_3[0], steiner1_coor_3[1], s=20, c="orange")
        steiner2_3=main_fig.scatter(steiner2_coor_3[0],steiner2_coor_3[1], s=20, c="orange")
        final_s1c=draw_line([S4x_initial_3[2],S4y_initial_3[2]],steiner1_coor_3)
        final_s1d=draw_line([S4x_initial_3[3],S4y_initial_3[3]],steiner1_coor_3)
        final_s1s2=draw_line(steiner1_coor_3,steiner2_coor_3)
        final_s2a=draw_line([S4x_initial_3[0],S4y_initial_3[0]],steiner2_coor_3)
        final_s2b=draw_line([S4x_initial_3[1],S4y_initial_3[1]],steiner2_coor_3)

        #text
        txt1_3 = main_fig.text(S4x_initial_3[0]-18, S4y_initial_3[0]+0.25, "A")
        txt2_3 = main_fig.text(S4x_initial_3[1]-10, S4y_initial_3[1]+4, "B")
        txt3_3 = main_fig.text(S4x_initial_3[2]+3, S4y_initial_3[2]-0.25, "C")
        txt4_3 = main_fig.text(S4x_initial_3[3]-14, S4y_initial_3[3]+0.25, "D")
        txt5_3 = main_fig.text(steiner2_coor_3[0]-20, steiner2_coor_3[1]+7, "S₂")
        txt6_3 = main_fig.text(steiner1_coor_3[0]-27, steiner1_coor_3[1]-2, "S₁")
        all_text+=[txt1_3,txt2_3,txt3_3,txt4_3,txt5_3,txt6_3]


        # Collect all required points/text/segments into given list
        all_points4_1=[S4all_points_1,S4all_points_2,S4all_points_3,S4e1_1,S4e3_1,S4e1_2,steiner1_1,steiner1_2,steiner2_2,steiner1_3,steiner2_3]
        all_text4_1=all_text

        if steiner_tree=='1':
            all_shapes4_1=e1ce3+s1e1_1+s1e1_2+s2s1+abe1+final_s1c+final_s1d+final_s1s2+final_s2a+final_s2b+s1d_1+s1d_2+s1c_1+s1c_2+s2b+s2c+[heinens_method_shapes_1[0],heinens_method_shapes_1[1][0],heinens_method_shapes_1[2],heinens_method_shapes_1[3][0]]
        
        if steiner_tree=='2':
            all_shapes4_1=e1ce3+s1e1_2+abe1+final_s1c+final_s1d+final_s1s2+final_s2a+final_s2b+s1d_2+s1c_2+[heinens_method_shapes_1[0],heinens_method_shapes_1[1][0],heinens_method_shapes_1[2],heinens_method_shapes_1[3][0]]
    
    def step_4_2(self,event):
        global heinens_method_shapes_2, all_points4_2, all_text4_2, all_shapes4_2
        heinens_method_shapes_2=[]

        # Remove all previous elements from step 3
        remove(all_points4_1,all_text4_1,all_shapes4_1)

        list_initialpoints_4_2=calculate_initialPOINTS(width/4,3*height/4,3)
        x_initial_4_2 = list_initialpoints_4_2[0]
        y_initial_4_2 = list_initialpoints_4_2[1]
        all_points_4_2 = main_fig.scatter(x_initial_4_2[2:], y_initial_4_2[2:], s=10, c="blue")

        S4e1,S4e2,S4e1_coor,S4e2_coor,x,x = triangle_drawing_steps([x_initial_4_2[0],y_initial_4_2[0]], [x_initial_4_2[1],y_initial_4_2[1]], [x_initial_4_2[0],y_initial_4_2[0]], [x_initial_4_2[1],y_initial_4_2[1]],[1,1],False)
        S4e1.remove()


        S4e3,S4e4,S4e3_coor,S4e4_coor,e3e2c,e4e2c = triangle_drawing_steps(S4e2_coor, [x_initial_4_2[2],y_initial_4_2[2]], S4e2_coor, [x_initial_4_2[2],y_initial_4_2[2]],[1,1],True)
            
        if steiner_tree=='1':
            S4e4.remove()
            for line in e4e2c:
                line.remove()
        
        elif steiner_tree=='2':
            S4e3.remove()
            for line in e3e2c:
                line.remove()
            
            S4e3=S4e4
            e3e2c=e4e2c
            S4e3_coor=S4e4_coor

        
        # Heinen's method
        s1d,s1c,s1e1,steiner1, steiner1_coor,heinens_method_shapes_2 = Heinens_Method(S4e2_coor,S4e3_coor, [x_initial_4_2[2],y_initial_4_2[2]], [x_initial_4_2[3],y_initial_4_2[3]], True, heinens_method_shapes_2)

        txtE2 = main_fig.text(S4e2_coor[0]-10, S4e2_coor[1]-25, "E₂")
        txtE3 = main_fig.text(S4e3_coor[0]-10, S4e3_coor[1]+6, "E₃")
        txtC = main_fig.text(x_initial_4_2[2]+8, y_initial_4_2[2]-1, "C")
        txtD = main_fig.text(x_initial_4_2[3]+5, y_initial_4_2[3]-5, "D")
        txtS1 = main_fig.text(steiner1_coor[0]-30, steiner1_coor[1]-4, "S₂")

        all_points4_2=[all_points_4_2,steiner1]
        all_text4_2=[txtE2,txtE3,txtC,txtD,txtS1]
        all_shapes4_2=e3e2c+[S4e2,S4e3,heinens_method_shapes_2[0],heinens_method_shapes_2[1][0]]

    def final_result(self,event):
        remove(all_points4_2, all_text4_2, all_shapes4_2)
        heinens_method_shapes_3=[]
        s=3
        S5list_initialpoints=calculate_initialPOINTS(width/3,2*height/3,s)

        S5x_initial = S5list_initialpoints[0]
        S5y_initial = S5list_initialpoints[1]
        main_fig.scatter(S5x_initial, S5y_initial, s=10, c="blue")

        # Draw diagram 1
        S5e1,S5e2,S5e1_coor,x,x,x = triangle_drawing_steps([S5x_initial[0],S5y_initial[0]], [S5x_initial[1],S5y_initial[1]], [S5x_initial[0],S5y_initial[0]], [S5x_initial[1],S5y_initial[1]],[1,1],False)
        S5e2.remove()
        S5e1.remove()

        if steiner_tree=='1':
            S5e3,S5e4,S5e3_coor,S5e4_coor,x,x = triangle_drawing_steps(S5e1_coor, [S5x_initial[2],S5y_initial[2]], S5e1_coor, [S5x_initial[2],S5y_initial[2]],[1,1],False)
            S5e4.remove()
        
        elif steiner_tree=='2':
            S5e3,S5e4,S5e3_coor,S5e4_coor,x,x = triangle_drawing_steps(S5e1_coor, [S5x_initial[2],S5y_initial[2]], S5e1_coor, [S5x_initial[2],S5y_initial[2]],[1,-1],False)
            S5e3.remove()

            S5e3_coor=S5e4_coor
            S5e3=S5e4
        

        x,x,x,x, steiner1_coor,heinens_method_shapes_3 = Heinens_Method(S5e1_coor,S5e3_coor, [S5x_initial[2],S5y_initial[2]], [S5x_initial[3],S5y_initial[3]], False,heinens_method_shapes_3)
        x,x,x,x, steiner2_coor,heinens_method_shapes_3 = Heinens_Method([S5x_initial[0],S5y_initial[0]],S5e1_coor, [S5x_initial[1],S5y_initial[1]], steiner1_coor, False,heinens_method_shapes_3)

        steiner1_3=main_fig.scatter(steiner1_coor[0], steiner1_coor[1], s=20, c="orange")
        steiner2_3=main_fig.scatter(steiner2_coor[0],steiner2_coor[1], s=20, c="orange")
        final_s1c=draw_line([S5x_initial[2],S5y_initial[2]],steiner1_coor)
        final_s1d=draw_line([S5x_initial[3],S5y_initial[3]],steiner1_coor)
        final_s1s2=draw_line(steiner1_coor,steiner2_coor)
        final_s2a=draw_line([S5x_initial[0],S5y_initial[0]],steiner2_coor)
        final_s2b=draw_line([S5x_initial[1],S5y_initial[1]],steiner2_coor)


        #text
        if steiner_tree=='1':
            txt1 = main_fig.text(S5x_initial[0]-20, S5y_initial[0]+0.25, "A")
            txt2 = main_fig.text(S5x_initial[1]+3, S5y_initial[1]-0.25, "B")
            txt3 = main_fig.text(S5x_initial[2]+3, S5y_initial[2]+0.25, "C")
            txt4 = main_fig.text(S5x_initial[3]-20, S5y_initial[3], "D")
            txt5 = main_fig.text(steiner2_coor[0]-20, steiner2_coor[1]+8, "S₂")
            txt6 = main_fig.text(steiner1_coor[0]-27, steiner1_coor[1]-2, "S₁")
        else:
            txt1 = main_fig.text(S5x_initial[0]-18, S5y_initial[0]+0.25, "B")
            txt2 = main_fig.text(S5x_initial[1]+3, S5y_initial[1]-0.25, "C")
            txt3 = main_fig.text(S5x_initial[2]-20, S5y_initial[2]-8, "D")
            txt4 = main_fig.text(S5x_initial[3]-20, S5y_initial[3]-5, "A")
            txt5 = main_fig.text(steiner2_coor[0]-25, steiner2_coor[1]+2, "S₂")
            txt6 = main_fig.text(steiner1_coor[0]-25, steiner1_coor[1]-13, "S₁")

        # calculate total_distance
        dist_as2=calculate_distance(S5x_initial[0],S5y_initial[0],steiner2_coor[0],steiner2_coor[1])
        dist_bs2=calculate_distance(S5x_initial[1],S5y_initial[1],steiner2_coor[0],steiner2_coor[1])
        dist_s1s2=calculate_distance(steiner1_coor[0],steiner1_coor[1],steiner2_coor[0],steiner2_coor[1])
        dist_cs1=calculate_distance(S5x_initial[2],S5y_initial[2],steiner1_coor[0],steiner1_coor[1])
        dist_ds1=calculate_distance(S5x_initial[3],S5y_initial[3],steiner1_coor[0],steiner1_coor[1])
        print(dist_as2/s,dist_bs2/s,dist_s1s2/s,dist_cs1/s,dist_ds1/s)
        total_distance=dist_as2+dist_bs2+dist_s1s2+dist_cs1+dist_ds1
        total_distance = total_distance/s
        main_fig.text(900,50,"Total distance = "+str(round(total_distance,2)))


# make choice about whether to create steiner tree 1 or 2
steiner_tree = input("Draw Steiner Tree 1 or 2: ")
# CREATE PLOT
main_fig = plt.subplot(111)
plt.subplots_adjust(bottom=0.2)
#self.day_text = self.axes.annotate(
        #    "Day 0", xy=[width/2, height], ha="center", va="bottom")
#self.axes = self.fig.add_subplot(111)
#self.axes.grid(False)
#self.axes.set_xticklabels([])
#self.axes.set_yticklabels([])
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

melzak_algo = Shape()     # create instance of class "Shape"

# create buttons
axstep0 = plt.axes([0.15, 0.05, 0.075, 0.05])   # parameters: x, y, width, height 
axstep1 = plt.axes([0.26, 0.05, 0.075, 0.05])
axstep2 = plt.axes([0.37, 0.05, 0.075, 0.05])
axstep3 = plt.axes([0.48, 0.05, 0.075, 0.05])
axstep4 = plt.axes([0.59, 0.05, 0.075, 0.05])
axstep5 = plt.axes([0.70, 0.05, 0.075, 0.05])
axstep6 = plt.axes([0.81, 0.05, 0.075, 0.05])
b0 = Button(axstep0, 'Initialise')     # parameters: placement of button, name written on button
b1 = Button(axstep1, 'Step1')
b2 = Button(axstep2, 'Step2')
b3 = Button(axstep3, 'Step3')
b4 = Button(axstep4, 'Step4')
b5 = Button(axstep5, 'Step4.5')
b6 = Button(axstep6, 'Final')

# If you click button, perform function in instance "melzak_algo" of class
b0.on_clicked(melzak_algo.step_0)
b1.on_clicked(melzak_algo.step_1)
b2.on_clicked(melzak_algo.step_2)
b3.on_clicked(melzak_algo.step_3)
b4.on_clicked(melzak_algo.step_4_1)
b5.on_clicked(melzak_algo.step_4_2)
b6.on_clicked(melzak_algo.final_result)

# Show the plot after running through code
plt.show()
