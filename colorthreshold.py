import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def gray(img):
   return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresh(img, thresh=(0,255)):
    binary = np.zeros_like(img)
    binary[(img > thresh[0]) & (img <= thresh[1])] = 1
    return binary

def rgb(img):
    #The RGB sequence is reversed as cv2.imread is used instead of mpimg.imread
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]
    return R, G, B

def hls(img):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    H = hls[:,:,0]
    L = hls[:,:,1]
    S = hls[:,:,2]
    return H, L, S

color_threshold_plot = plt.figure(figsize=(9,18))

def add_to_plot(img, label, count, color=False):
    axis = color_threshold_plot.add_subplot(3,4,count)
    axis.set_xlabel(label)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    if color:
        axis.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        axis.imshow(img, cmap="gray")

path2 = "test_images/"
file = "test6.jpg"

img = cv2.imread(path2+file)
add_to_plot(img, "Source", 1, True)

gray = gray(img)
add_to_plot(gray, "Grayscale", 2)

graythresh = thresh(gray, thresh=(180,255))
add_to_plot(graythresh, "Gray thresh", 3)

R, G, B = rgb(img)
r_thresh = thresh(R, thresh=(200,255))
g_thresh = thresh(G, thresh=(200,255))
b_thresh = thresh(B, thresh=(200,255))


add_to_plot(g_thresh, "G thresh", 5)
add_to_plot(b_thresh, "B thresh", 6)

H, L, S = hls(img)
h_thresh = thresh(H, thresh=(15,100))
l_thresh = thresh(L, thresh=(90,255))
s_thresh = thresh(S, thresh=(90,255))

add_to_plot(l_thresh, "L thresh", 7)
add_to_plot(h_thresh, "H thresh", 8)


combined = np.zeros_like(s_thresh)
combined[((r_thresh==1)|(s_thresh==1))] = 1

add_to_plot(r_thresh, "R thresh", 9)
add_to_plot(s_thresh, "S thresh", 10)
add_to_plot(combined, "Combined R and S Thresh", 11)

plt.tight_layout(h_pad=0, w_pad=0)
plt.show()
color_threshold_plot.savefig('output_images/color_threshold_plot.png')
