import cv2
import numpy as np

print "Disparity Estiamtion"
left_img = cv2.imread('view1.png', 0)  #read it as a grayscale image
right_img = cv2.imread('view5.png', 0)

#Disparity Computation for Left Image

disparityMat = np.zeros(shape = left_img.shape, dtype='uint8')

for row in range(left_img.shape[0]):
    
#     print row

    occlusionCost = 20 #(You can adjust this, depending on how much threshold you want to give for noise)
    
    #For Dynamic Programming you have build a cost matrix. Its dimension will be numcols x numcols
    
    numcols = left_img.shape[1]
    
    costMatrix = np.zeros(shape=(numcols,numcols))
    directionMatrix = np.zeros(shape=(numcols,numcols))  #(This is important in Dynamic Programming. You need to know which direction you need traverse)
    
    #We first populate the first row and column values of Cost Matrix
    
    for i in range(numcols):
        costMatrix[i,0] = i*occlusionCost
        costMatrix[0,i] = i*occlusionCost
    
    
    
    z1 = left_img[row,:]
    z2 = right_img[row,:]
        
    for i in range(1, numcols):
        for j in range(1, numcols):
            min1 = costMatrix[i-1,j-1] + abs(z1[i]-z2[j])
            min2 = costMatrix[i-1,j] + occlusionCost
            min3 = costMatrix[i,j-1] + occlusionCost 
            costMatrix[i,j] = min(min1,min2,min3)
            if min1 == costMatrix[i,j]:
                directionMatrix[i,j] = 1
            elif min2 == costMatrix[i,j]:
                directionMatrix[i,j] = 2
            else:
                directionMatrix[i,j] = 3
    
    
    p = numcols-1
    q = p
    cntr = 0
    while p > 0 and q > 0:
        temp = directionMatrix[p,q]
        if temp == 1:
            disparityMat[row,p] = p - q
            p -= 1
            q -= 1
        elif temp == 2:
            p -= 1
        else:
            q -= 1
            

# min = np.min(disparityMat)
# diff = np.max(disparityMat) - np.min(disparityMat)
# disparityMat = np.array([((x - min)/diff) for x in disparityMat])

cv2.imshow('dispMat', disparityMat)  
cv2.imwrite('DPDisparityMatrix.jpg', disparityMat)
cv2.waitKey(0)
cv2.destroyAllWindows()
