import cv2
import numpy as np
import sys

def leftDispEst(left_img, right_img, pad):

    leftDisparityMat = np.zeros(shape = left_img.shape, dtype = "uint8")
    left_img = cv2.copyMakeBorder(left_img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, 0)
    right_img = cv2.copyMakeBorder(right_img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, 0)


    for i in range(pad, left_img.shape[0] - pad):
#         print i
        for j in range(pad, left_img.shape[1] - pad):
    #         print i, j
            local_min = sys.maxint
            min_index = j
            leftTemp = left_img[i-pad:i+pad+1:, j-pad:j+pad+1:]
#             print leftTemp
            k = j
            while(j-k < 75) and (k!=pad):
    #             print left_img[i-pad:i+pad+1:, j-pad:j+pad+1:]
#                 print right_img[i-pad:i+pad+1:, k-pad:k+pad+1:]
                tempSum = np.sum((leftTemp - right_img[i-pad:i+pad+1:, k-pad:k+pad+1:])**2)
                if tempSum < local_min:
                    local_min = tempSum
                    min_index = k
                 
                k = k - 1
                 
            leftDisparityMat[i-pad][j-pad] = j - min_index
    
    return leftDisparityMat

def rightDispEst(left_img, right_img, pad):

    rightDisparityMat = np.zeros(shape = right_img.shape, dtype = "uint8")
    right_img = cv2.copyMakeBorder(right_img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, 0)
    left_img = cv2.copyMakeBorder(left_img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, 0)


    for i in range(pad, right_img.shape[0] - pad):
#         print i
        for j in range(pad, right_img.shape[1] - pad):
    #         print i, j
            local_min = sys.maxint
            min_index = j
            rightTemp = right_img[i-pad:i+pad+1:, j-pad:j+pad+1:]
            k = j
            while(k-j < 75) and (k < (right_img.shape[1] - pad)):
    #             print left_img[i-pad:i+pad+1:, j-pad:j+pad+1:]
    #             print right_img[i-pad:i+pad+1:, k-pad:k+pad+1:]
                tempSum = np.sum((rightTemp - left_img[i-pad:i+pad+1:, k-pad:k+pad+1:])**2)
                
                if tempSum < local_min:
                    local_min = tempSum
                    min_index = k
                 
                k = k + 1
                 
            rightDisparityMat[i-pad][j-pad] = min_index - j
    
    
    return rightDisparityMat

if __name__ == "__main__":
    left_img = cv2.imread('view1.png', 0)
    right_img = cv2.imread('view5.png', 0)

    gdLeft = cv2.imread('disp1.png', 0)
    gdRight = cv2.imread('disp5.png', 0)
    
    
    leftDisparityMatrix = leftDispEst(left_img, right_img, 1)
    rightDisparityMatrix = rightDispEst(left_img, right_img, 1)
    
    
    cv2.imshow('LeftDispMat3x3', leftDisparityMatrix) 
    cv2.imshow('RigthDispMat3x3', rightDisparityMatrix)  
     
    cv2.imwrite('LeftDispMat3x3.jpg',leftDisparityMatrix)
    cv2.imwrite('RightDispMat3x3.jpg',rightDisparityMatrix)
    
    print "MSE for Left Disparity Matrix before Consistency check for 3x3 ", np.mean((gdLeft - leftDisparityMatrix)**2)
    print "MSE for Right Disparity Matrix before Consistency check for 3x3 ", np.mean((gdRight - rightDisparityMatrix)**2)
    
    #Consistency check
    leftDisparityMatrixC = np.zeros(shape = left_img.shape, dtype = "uint8")
    for i in range(0, left_img.shape[0]):
        for j in range(0, left_img.shape[1]):
            if (rightDisparityMatrix[i][j - leftDisparityMatrix[i][j]]) != (leftDisparityMatrix[i][j]):
                leftDisparityMatrixC[i][j] = 0
                gdLeft[i][j] = 0
            else:
                leftDisparityMatrixC[i][j] = leftDisparityMatrix[i][j]
                  
    rightDisparityMatrixC = np.zeros(shape = left_img.shape, dtype = "uint8")
    for i in range(0, left_img.shape[0]):
        for j in range(0, left_img.shape[1]):
            if (leftDisparityMatrix[i][j + rightDisparityMatrix[i][j]]) != (rightDisparityMatrix[i][j]):
                rightDisparityMatrixC[i][j] = 0
                gdRight[i][j] = 0
            else:
                rightDisparityMatrixC[i][j] = rightDisparityMatrix[i][j]
    
    
    cv2.imshow('LeftDispMat3x3CC', leftDisparityMatrixC) 
    cv2.imshow('RigthDispMat3x3CC', rightDisparityMatrixC)
    cv2.imwrite('LeftDispMat3x3CC.jpg',leftDisparityMatrixC)
    cv2.imwrite('RightDispMat3x3CC.jpg',rightDisparityMatrixC)
    
    print "MSE for Left Disparity Matrix after Consistency check for 3x3 ", np.mean((gdLeft - leftDisparityMatrixC)**2)
    print "MSE for Right Disparity Matrix after Consistency check for 3x3 ", np.mean((gdRight - rightDisparityMatrixC)**2)
    
    #9x9 block
    gdLeft = cv2.imread('disp1.png', 0)
    gdRight = cv2.imread('disp5.png', 0)
    
    leftDisparityMatrix = leftDispEst(left_img, right_img, 4)
    rightDisparityMatrix = rightDispEst(left_img, right_img, 4)
    cv2.imshow('LeftDispMat9x9', leftDisparityMatrix) 
    cv2.imshow('RigthDispMat9x9', rightDisparityMatrix)  
      
    cv2.imwrite('LeftDispMat9x9.jpg',leftDisparityMatrix)
    cv2.imwrite('RightDispMat9x9.jpg',rightDisparityMatrix)
     
     
    print "MSE for Left Disparity Matrix before Consistency check for 9x9 ", np.mean((gdLeft - leftDisparityMatrix)**2)
    print "MSE for Right Disparity Matrix before Consistency check for 9x9 ", np.mean((gdRight - rightDisparityMatrix)**2)
     
     
    #Consistency check
    leftDisparityMatrixC = np.zeros(shape = left_img.shape, dtype = "uint8")
    for i in range(0, left_img.shape[0]):
        for j in range(0, left_img.shape[1]):
            if (rightDisparityMatrix[i][j - leftDisparityMatrix[i][j]]) != (leftDisparityMatrix[i][j]):
                leftDisparityMatrixC[i][j] = 0
                gdLeft[i][j] = 0
            else:
                leftDisparityMatrixC[i][j] = leftDisparityMatrix[i][j]
            
    rightDisparityMatrixC = np.zeros(shape = left_img.shape, dtype = "uint8")
    for i in range(0, left_img.shape[0]):
        for j in range(0, left_img.shape[1]):
            if (leftDisparityMatrix[i][j + rightDisparityMatrix[i][j]]) != (rightDisparityMatrix[i][j]):
                rightDisparityMatrixC[i][j] = 0
                gdRight[i][j] = 0
            else:
                rightDisparityMatrixC[i][j] = rightDisparityMatrix[i][j]
     
    cv2.imshow('LeftDispMat9x9CC', leftDisparityMatrixC) 
    cv2.imshow('RigthDispMat9x9CC', rightDisparityMatrixC)
    cv2.imwrite('LeftDispMat9x9CC.jpg',leftDisparityMatrixC)
    cv2.imwrite('rRightDispMat9x9CC.jpg',rightDisparityMatrixC)
    print "MSE for Left Disparity Matrix after Consistency check for 9x9 ", np.mean((gdLeft - leftDisparityMatrixC)**2)
    print "MSE for Right Disparity Matrix after Consistency check for 9x9 ", np.mean((gdRight - rightDisparityMatrixC)**2)
     
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    