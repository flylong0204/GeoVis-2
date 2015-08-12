import numpy as np
from skimage import segmentation
from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
from math import sqrt

class NodeCluster:
    def __init__(self):
        self.labelIndex = []
    
    def reindexLabels(self, img):
        height, width = img.shape[:2]
        seqIndex = {}
        for h in range(0, height):
            for w in range(0, width):
                currentLabel = self.pixelLabelIndex[h, w]
                if (seqIndex.get(currentLabel) == None):
                    newLabelIndex = {}
                    newLabelIndex['label'] = currentLabel
                    newLabelIndex['x'] = w
                    newLabelIndex['y'] = h
                    newLabelIndex['nodeNum'] = 1
                    newLabelIndex['mean'] = float(self.image[h, w])
                    newLabelIndex['var'] = 0
                    self.labelIndex.append(newLabelIndex)
                    seqIndex[currentLabel] = self.labelIndex.index(newLabelIndex, )
                else:
                    tempIndex = seqIndex[currentLabel]
                    self.labelIndex[tempIndex]['x'] += w
                    self.labelIndex[tempIndex]['y'] += h
                    self.labelIndex[tempIndex]['nodeNum'] += 1
                    self.labelIndex[tempIndex]['mean'] += self.image[h, w]
        for index in self.labelIndex:
            index['x'] /= float(index['nodeNum'])
            index['y'] /= float(index['nodeNum'])
            index['mean'] /= float(index['nodeNum'])
        for h in range(0, height):
            for w in range(0, width):
                currentLabel = self.pixelLabelIndex[h, w]
                index = self.labelIndex[seqIndex[currentLabel]]
                index['var'] += pow(self.image[h, w] - index['mean'], 2)
        for index in self.labelIndex:
            index['var'] = sqrt(index['var'] / float(index['nodeNum']))
    
    def processImage(self, img, segCount):
        self.image = img
        self.pixelLabelIndex = segmentation.slic(img, compactness=30, n_segments=segCount)
        self.reindexLabels(img)
            
    def processImageHier(self, img, segCount):
        self.image = img
        x = np.reshape(img, (-1, 1))
        connectivity = grid_to_graph(*img.shape[:2])
        ward = AgglomerativeClustering(n_clusters=segCount, linkage='ward', connectivity=connectivity).fit(x)
        self.pixelLabelIndex = np.reshape(ward.labels_, img.shape[:2])
        print self.pixelLabelIndex.size
        print np.unique(self.pixelLabelIndex).size
        self.reindexLabels(img)

class OverlayProcessor:
    def __init__(self, nodes):
        self.nodes = nodes
        self.nodeNum = nodes.lables.length()
    
    def setCurrentLevel(self, level):
        self.currentLevel = level
    
    def updateParameters(self):
        self.a = np.identity(self.nodeNum, np.float32)
        #S: candidate sites, which are self.nodes at different levels
        #T: test nodes, which are self.nodes
        #a: if CSi can be accessed by CSj
        #W: data volume
        #CA: data join cost
        #CE: data visualization cost
        #CI: glyph visualization cost
        #Z: if a glyph is positioned
        #x: if TNi is assigned to CSj\
        S = []
        for index in self.nodes.labelIndex:
            for level in range(0, 5):
                newSite = {}
                newSite['x'] = index['x']
                newSite['y'] = index['y']
                newSite['level'] = level
                index['mean'] = 0
                index['var'] = 0
                index['nodeNum'] = 0
                S.append(newSite)
                
        a = np.zeros((len(self.nodes), len(S)), np.uint8)
        for i in range(0, len(self.nodes)):
            for j in range(0, len(S)):
                node = self.nodes[i]
                site = S[j]
                distance = sqrt(pow(node['x'] - site['x'], 2) + pow(node['y'] - site['y']))
                if (distance < site['level']):
                    a[i][j] = 1
        #Update site mean and variance            
        for i in range(0, len(self.nodes)):
            for j in range(0, len(S)):
                if (a[i][j] == 1):
                    S[j]['mean'] += self.nodes[j]['mean']
                    S[j]['nodeNum'] += 1
        for i in range(0, len(S)):
            S[i]['mean'] /= float(S[i]['nodeNum'])
        for i in range(0, len(self.nodes)):
            for j in range(0, len(S)):
                S[j]['var'] += pow(self.nodes[i]['mean'] - S[j]['mean'], 2)
        for i in range(0, len(S)):
            S[i]['var'] /= float(S[i]['nodeNum'])
        
        w = np.zeros(len(self.nodes), np.float32)
        for i in range(0, len(w)):
            w[i] = self.nodes[i]['nodeNum']
            
        ca = np.zeros((len(self.nodes), len(S)), np.float32)
        for i in range(0, len(self.nodes)):
            for j in range(0, len(S)):
                ca[i][j] = abs(self.nodes[i]['mean'] - S[j]['mean'])
        
        ce = np.zeros((len(self.nodes), len(S)), np.float32)
        for i in range(0, len(self.nodes)):
            for j in range(0, len(S)):
                ce[i][j] = abs(self.nodes[i]['var'] - S[j]['var'])
                
        ci = np.zeros(len(S), np.float32)
        for i in range(0, len(S)):
            ci[i] =  abs(S[i]['level'] - self.currentLevel)
            
        z = np.zeros(len(S), np.uint8)
        x = np.zeros((len(self.nodes), len(S)), np.uint8)
        
    
    def heuristicSolve(self):
        minCost = 0.0
        self.updateParameters()
        #TODO: integer programming
        return minCost

