import numpy as np
import cv2


if __name__ == "__main__":
    
    left_img = cv2.imread('view1.png')
    right_img = cv2.imread('view5.png')

    centerImg = np.zeros(shape = left_img.shape, dtype = "uint8")
    centerImg1 = np.zeros(shape = left_img.shape, dtype = "uint8")
    centerImg2 = np.zeros(shape = left_img.shape, dtype = "uint8")

    gdl = cv2.imread('disp1.png', 0)
    gdr = cv2.imread('disp5.png', 0)
    
    for i in range(0, left_img.shape[0]):
        for j in range(0, left_img.shape[1]):
            k = int(gdl[i,j]/2)
            if (j - k) > 0:
                centerImg1[i][j - k] = left_img[i][j]
                
                
    for i in range(0, right_img.shape[0]):
        for j in range(0, right_img.shape[1]):
            k = int(gdr[i,j]/2)
            if (j + k) < right_img.shape[1]:
                centerImg2[i][j + k] = right_img[i][j]
                
    for i in range(0, centerImg1.shape[0]):
        for j in range(0, centerImg2.shape[1]):
            if (centerImg1[i][j][0] == 0) and (centerImg1[i][j][1] == 0) and (centerImg1[i][j][2] == 0):
                centerImg[i][j] = centerImg2[i][j]
            else:
                centerImg[i][j] = centerImg1[i][j] 
    
    cv2.imshow('leftSyn', centerImg1)  
    cv2.imshow('rightSyn', centerImg2)  
    cv2.imshow('centerSyn', centerImg)
    cv2.imwrite('leftSyn.jpg', centerImg1)  
    cv2.imwrite('rightSyn.jpg', centerImg2)  
    cv2.imwrite('centerSyn.jpg', centerImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()