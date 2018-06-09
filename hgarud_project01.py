import json
import numpy as np
from scipy.linalg import eig
import cv2

img= cv2.imread('/home/hrishi/1Hrishi/2Git/Single_View_Metrology/images/input/s8_test.jpg')

def getPoints(image_name, index):
    path = "/home/hrishi/1Hrishi/2Git/Single_View_Metrology"
    fname = image_name + ".json"
    with open(fname) as data_file:
        data = json.load(data_file)
    return np.array(data["shapes"][index]["points"])

def homogenize(points):
    z = np.ones((6,1))
    return np.append(points, z, 1)

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

# Find intersection point of two lines (not segments!)
def line_intersection(line1, line2):
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(x_diff, y_diff)
    if div == 0:
        return None  # Lines don't cross

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div

    return x, y, 1

def x_vanish(points):
    #temp = np.cross(np.cross(points[0,:], points[1,:]),
     #               np.cross(points[5,:], points[2,:]))

	temp = line_intersection((points[0,:], points[1,:]), (points[5,:], points[2,:]))

	#return temp/temp[2]
	return temp
def y_vanish(points):
    #temp = np.cross(np.cross(points[2,:], points[3,:]),
    #                np.cross(points[5,:], points[4,:]))
    #return temp/temp[2]
	temp = line_intersection((points[2,:], points[3,:]), (points[5,:], points[4,:]))
	return temp
def z_vanish(points):
    #temp = np.cross(np.cross(points[0,:], points[5,:]),
    #                np.cross(points[1,:], points[2,:]))
    #return temp/temp[2]
    temp = line_intersection((points[0,:], points[5,:]), (points[1,:], points[2,:]))
    return temp

points = getPoints("s8_test", 0)
image_size = [3007, 2681]

#Center of the image as origin
points[:,0] = points[:,0] - ((image_size[0])/2)
points[:,1] = points[:,1] - ((image_size[1])/2)

#Closest point of the box as the origin
points[:,0] = points[:,0] - points[0,0]
points[:,1] = points[:,1] + points[0,1]

points_homo = homogenize(points)

V_x = np.array(x_vanish(points_homo))
V_y = np.array(y_vanish(points_homo))
V_z = np.array(z_vanish(points_homo))

Wo = np.array([1631.5,2596.5,1])

ref_x = np.array([2711.5,1016.5,1]);
ref_y = np.array([415,1900,1]);
ref_z = np.array([1603.5,1892.5,1]);

ref_x_dis = 16*15;
ref_y_dis = 8.5*15;
ref_z_dis = 5.3*15;

Vx1 = np.array([V_x - ref_x]).T
Vy1 = np.array([V_y - ref_y]).T
Vz1 = np.array([V_z - ref_z]).T

a_x,l, m, n= np.linalg.lstsq((Vx1) , (ref_x - Wo))
a_y,l, m, n= np.linalg.lstsq((Vy1) , (ref_y - Wo))
a_z,l, m, n= np.linalg.lstsq((Vz1) , (ref_z - Wo))

alpha_x = a_x / ref_x_dis
alpha_y = a_y / ref_y_dis
alpha_z = a_z / ref_z_dis

Px = V_x*alpha_x
Py = V_y*alpha_y
Pz = V_z*alpha_z

P=np.zeros((3,4))

P[:,0] = Px
P[:,1] = Py
P[:,2] = Pz
P[:,3] = Wo

Hxy=np.zeros((3,3))
Hyz=np.zeros((3,3))
Hxz=np.zeros((3,3))

Hxy[:,0] = Px
Hxy[:,1] = Py
Hxy[:,2] = Wo

Hxy[0,2] = Hxy[0,2] - 800
Hxy[0,2] = Hxy[0,2] + 900


Hyz[:,0] = Py
Hyz[:,1] = Pz
Hyz[:,2] = Wo*2

Hyz[0,2]=Hyz[0,2] + 2000
Hyz[1,2]=Hyz[1,2] + 2000

Hxz[:,0] = Px
Hxz[:,1] = Pz
Hxz[:,2] = Wo*0.5

Hxz[0,2]=Hxz[0,2] - 5000
Hxz[1,2]=Hxz[1,2] + 9000

a,b,c=img.shape

XY = cv2.warpPerspective(img,Hxy,(a,b), flags = cv2.WARP_INVERSE_MAP)
YZ = cv2.warpPerspective(img,Hyz,(a,b), flags = cv2.WARP_INVERSE_MAP)
XZ = cv2.warpPerspective(img,Hxz,(a,b), flags = cv2.WARP_INVERSE_MAP)

cv2.imwrite("XY_homography.png", XY)
cv2.imwrite("YZ_homography.png", YZ)
cv2.imwrite("XZ_homography.png", XZ)

cv2.imshow("Txy",XY)
cv2.imshow("Tyz",YZ)
cv2.imshow("Txz",XZ)

cv2.waitKey(0)
