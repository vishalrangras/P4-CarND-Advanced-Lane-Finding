import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

imgpoints = [] # 2D points in image plane
objpoints = [] # 3D points in real world space

objp = np.zeros((6*9,3),np.float32)
objp[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2) # x, y coordinate

corner_images = []
def draw_corners(chessimage):
    
    nx = 9
    ny = 6
    
    img = cv2.imread(chessimage)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        imgpoints.append(corners)
        objpoints.append(objp)
        cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
        corner_images.append(img)
    else:
        corner_images.append(img)

import os

for file in os.listdir("camera_cal/"):
    draw_corners("camera_cal/"+file)

corner_frame = plt.figure(figsize=(18,9))

for i in range(0, len(corner_images)):
    axis = corner_frame.add_subplot(4,5,i+1)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    axis.imshow(corner_images[i])
corner_frame.tight_layout(h_pad=0, w_pad=0)
corner_frame.savefig('corners.png')

#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#dst = cv2.undistort(img, mtx, dist, None, mtx) 

undistorted_images = []

def undistort_img(path, imgname, objpoints, imgpoints):
    img = cv2.imread(path+"/"+imgname)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[0:2], None, None)
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    cv2.imwrite(path+"/"+imgname[0:imgname.find('.')]+"u.jpg", undist)
    undistorted_images.append(undist)

import os

for file in os.listdir("camera_cal/"):
    undistort_img("camera_cal",file, objpoints, imgpoints)
    
undistorted_frame = plt.figure(figsize=(18,9))

for i in range(0, len(undistorted_images)):
    axis = undistorted_frame.add_subplot(4,5,i+1)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    axis.imshow(undistorted_images[i])
undistorted_frame.tight_layout(h_pad=0, w_pad=0)
undistorted_frame.savefig('undistorted_images.png')
