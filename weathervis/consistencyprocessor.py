import math

class ConsistencyProcessor:
    def __init__(self, candPos, levelNumber):
        self.name = 'Consistency processor'
        self.candPos = candPos
        self.candNumber = len(self.candPos)
        self.levelNumber = levelNumber
    
    def updateLevelData(self, level, candStatus, gamma):
        fL = [0 for x in range(self.levelNumber * self.candNumber)]
        
        for i in range(self.levelNumber):
            radius = pow(2, i + 1) / 2
            for j in range(self.candNumber):
                p = [0 for x in range(self.levelNumber + 1)]
                q = [0 for x in range(self.levelNumber + 1)]
                xp = self.candPos[j]['x']
                yp = self.candPos[j]['y']
                # construct lower level distribution
                if (i == 0):
                    p[0] = 1
                else:
                    for k in range(self.candNumber * self.levelNumber):
                        if (candStatus[i - 1][k] == 1):
                            levelIndex = k / self.candNumber
                            candIndex = k % self.candNumber
                            distance = math.sqrt(pow(self.candPos[candIndex]['x'] - xp, 2) + pow(self.candPos[candIndex]['y'] - yp, 2))
                            if (distance <= radius):
                                p[levelIndex] += 1
                # construct upper level distribution
                if (i == self.levelNumber - 1):
                    q[0] = 1
                else:
                    for k in range(self.candNumber * self.levelNumber):
                        if (candStatus[i + 1][k] == 1):
                            levelIndex = k / self.candNumber
                            candIndex = k % self.candNumber
                            distance = math.sqrt(pow(self.candPos[candIndex]['x'] - xp, 2) + pow(self.candPos[candIndex]['y'] - yp, 2))
                            if (distance <= radius):
                                q[levelIndex] += 1
                
                # update fl
                tempFL = 0
                sumCount = 0
                for pIndex in range(len(p)):
                    for qIndex in range(len(q)):
                        if (qIndex >= pIndex):
                            tempFL += p[pIndex] * q[qIndex] * math.exp(-1 * gamma * abs(i - (pIndex + qIndex) / 2.0))
                        sumCount += p[pIndex] * q[qIndex]
                if (sumCount != 0):
                    fL[i * self.candNumber + j] = tempFL / sumCount 
        return fL