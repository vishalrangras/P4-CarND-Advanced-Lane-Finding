import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def thresh(img, thresh=(0,255)):
    binary = np.zeros_like(img)
    binary[(img > thresh[0]) & (img <= thresh[1])] = 1
    return binary

def colorthresh(img):

    r_channel = img[:,:,2]
    r_thresh = thresh(r_channel, thresh=(200,255))

    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    s_thresh = thresh(s_channel, thresh=(90,255))

    color_combined = np.zeros_like(s_thresh)
    color_combined[((r_thresh==1)|(s_thresh==1))] = 1

    return color_combined

def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    if orient == 'x':
        sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    else:
        sobel = cv2.Sobel(img, cv2.CV_64F, 0, 1)

    abs_sobel = np.absolute(sobel)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    sbinary = np.zeros_like(scaled_sobel)
    sbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    return sbinary

def mag_thresh(img, sobel_kernel=9, mag_thresh=(30, 100)):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8) 
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1
    return binary_output

def dir_threshold(img, sobel_kernel=9, thresh=(0.7, 1.3)):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    binary_output =  np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1
    return binary_output

def gradthresh(img):
    gradx = abs_sobel_thresh(img, orient='x', thresh_min=20, thresh_max=120)
    grady = abs_sobel_thresh(img, orient='y', thresh_min=20, thresh_max=120)
    mag_binary = mag_thresh(img)
    dir_binary = dir_threshold(img)

    grad_combined = np.zeros_like(dir_binary)
    grad_combined[((gradx==1)&(grady==1))|((mag_binary == 1)&(dir_binary == 1))] = 1

    return grad_combined

path2 = "test_images/"
file = "test5.jpg"
img = cv2.imread(path2+file)

color_grad_threshold_plot = plt.figure(figsize=(6,12))

def add_to_plot(img, label, count, color=False):
    axis = color_grad_threshold_plot.add_subplot(3,2,count)
    axis.set_xlabel(label)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    if color:
        axis.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        axis.imshow(img, cmap="gray")

add_to_plot(img, "Source", 1, True)

color_thresh = colorthresh(img)
add_to_plot(color_thresh, "Color Threshold", 3)

grad_thresh = gradthresh(color_thresh)
add_to_plot(grad_thresh, "Gradient Threshold", 4)

color_binary = np.dstack(( np.zeros_like(grad_thresh), grad_thresh, color_thresh))
add_to_plot(color_binary, "Combined Stacked", 5)

combined_color_grad_binary = np.zeros_like(grad_thresh)
combined_color_grad_binary[(grad_thresh==1) | (color_thresh==1)] = 1
add_to_plot(combined_color_grad_binary, "Combined Threshold", 6)

plt.tight_layout(h_pad=0, w_pad=0)
plt.show()
color_grad_threshold_plot.savefig('output_images/color_grad_threshold_plot_2.png')
