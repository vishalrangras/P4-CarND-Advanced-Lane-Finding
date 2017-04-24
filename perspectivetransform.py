import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

'''
img = mpimg.imread("test_images/test6.jpg")

plt.imshow(img)

plt.plot(722, 446,".")
plt.plot(1115, 684,".")
plt.plot(285, 684,".")
plt.plot(630, 446,".")

plt.show()
'''

def warp(img):
    img_size = (img.shape[1], img.shape[0])

    #top right, bottom right, bottom left, top left


    src = np.float32([[490, 482],[810, 482], [1250, 720],[40, 720]])
    dst = np.float32([[0, 0], [1280, 0], [1250, 720],[40, 720]])
    
    #Use this one
    #src = np.float32([[722,446],[1115,684],[285, 684],[630, 446]])
    
    #src = np.float32([[768,478],[1115,684],[285, 684],[575, 478]])
    #src = np.float32([[730,453],[1102,668],[304, 668],[622, 453]])
    
    #dst = np.float32([[1115,235],[1115,684],[285, 684],[285, 235]])

    #Use this one
    #dst = np.float32([[1115,135],[1115,718],[285, 718],[285, 135]])
    
    M = cv2.getPerspectiveTransform(src, dst)

    Minv = cv2.getPerspectiveTransform(dst, src)

    warped_img = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    plt.imshow(warped_img)
    plt.show()
    return warped_img


path2 = "output_images/"
file = "combined_threshold_6.png"
img = cv2.imread(path2+file)

warped_img = warp(img)
cv2.imwrite("output_images/warped_binary.jpg",warped_img)
    
#285, 684
#- 1115, 684
#- 575, 478
#- 768, 478

#285, 235
#1115, 235
