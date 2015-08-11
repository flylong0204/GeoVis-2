import numpy as np
from matplotlib import pyplot as plt
import cv2


img = cv2.imread('water_coins.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
height, width = gray.shape[:2]
seedMap = np.zeros((height, width), np.uint8)
seedIndex = 0
for i in range(0, 4):
    for j in range(0, 4):
        beginX = j - 1
        if (beginX < 0): beginX = 0
        endX = j + 1
        if (endX >= width): endX = width - 1
        beginY = i - 1
        if (beginY < 0): beginY = 0
        endY = i + 1
        if (endY >= height): endY = height - 1
        isMinima = True
        for ii in range(beginY, endY + 1):
            for jj in range(beginX, endX + 1):
                if (ii == i and jj == j): continue
                if gray[ii, jj] < gray[i, j]: 
                    isMinima = False
                    break
        if (isMinima == True):
            seedIndex += 1
            seedMap[i, j] = 1
ret, markers = cv2.connectedComponents(seedMap)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers = cv2.watershed(img, markers)
img[markers == -1] = [0,255,0]
cv2.imshow('tes1', img)
cv2.waitKey(0)
cv2.destroyAllWindows()