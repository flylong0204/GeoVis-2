import math

class UncertaintyProcessor:
    def __init__(self, ens, h, w, data):
        self.ens = ens
        self.h = h
        self.w = w
        self.data = data
        
    def ProcessUnVolume(self, x, y, level):
        unResult = {}
        unResult['mean'] = 0
        unResult['var'] = 0
        
        level = pow(2, level) / 2
        
        left = int(x - level < 0 and 0 or (x - level))
        right = int(x + level >= self.w and (self.w - 1) or (x + level))
        bottom = int(y - level < 0 and 0 or (y - level))
        top = int(y + level >= self.h and (self.h - 1) or (y + level))
        
        for h in range(bottom, top + 1):
            for w in range(left, right + 1):
                for ens in range(0, self.ens):
                    unResult['mean'] += self.data[ens][h][w]
        nodeCount = (right - left + 1) * (top - bottom + 1) * self.ens
        unResult['mean'] /= nodeCount
        
        for h in range(bottom, top + 1):
            for w in range(left, right + 1):
                for ens in range(0, self.ens):
                    unResult['var'] += math.pow(self.data[ens][h][w] - unResult['mean'], 2)
        unResult['var'] = math.sqrt(unResult['var'] / (nodeCount * self.ens))
        return unResult
    