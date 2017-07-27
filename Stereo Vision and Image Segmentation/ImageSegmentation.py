import cv2
import numpy as np
import math

def featureMatrix(img):
    
    feaMat = np.zeros(shape=(img.shape[0] * img.shape[1], 5))
    cntr = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            feaMat[cntr] = np.concatenate((img[i][j], [i], [j]))
            cntr += 1 
    
    return feaMat

if __name__ == "__main__":
    print 'segment'
    img = cv2.imread('Butterfly.jpg')
    
    h = 90
    h = h*h
    iter = 10
    
    feaMat = featureMatrix(img)
    
    while(feaMat.shape[0] != 0):
        print "feaMat size ", feaMat.shape[0]
        meanDiff = iter + 1
        
        currentMean = feaMat[0]
#         segIndexes = [0]
        
        while(meanDiff > iter):
#             print "current meanDiff ", meanDiff
            segIndexes = []
            for i in range(0, feaMat.shape[0]):
                if np.sum((feaMat[i] - currentMean)**2) < h:
                    segIndexes = segIndexes + [i]
            
            segment = feaMat[segIndexes, :]
            
            newMean = np.mean(segment, axis=0)
#             print newMean
            meanDiff = math.sqrt(np.sum((newMean - currentMean)**2))
            currentMean = newMean
            
        
        for i in segIndexes:
            img[int(feaMat[i][3])][int(feaMat[i][4])] = currentMean[0:3]
        
        
        feaMat = np.delete(feaMat, segIndexes, axis=0)
        
        
    cv2.imshow('segment', img)  
    cv2.imwrite('segment13.jpg',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
        
        
        
        
    