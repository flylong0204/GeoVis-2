import numpy as np
from skimage import segmentation
from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
from math import sqrt
import cplex

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
        self.nodeNum = len(nodes.labelIndex)
        self.currentLevel = 1
    
    def setCurrentLevel(self, level):
        self.currentLevel = level
    
    def updateParameters(self):
        #S: candidate sites, which are self.nodes at different levels
        #T: test nodes, which are self.nodes
        #a: if CSi can be accessed by CSj
        #W: data volume
        #CA: data join cost
        #CE: data visualization cost
        #CI: glyph visualization cost
        #Z: if a glyph is positioned
        #x: if TNi is assigned to CSj\
        self.S = []
        for index in self.nodes.labelIndex:
            for level in range(0, 2):
                newSite = {}
                newSite['x'] = index['x']
                newSite['y'] = index['y']
                newSite['level'] = level
                newSite['mean'] = 0
                newSite['var'] = 0
                newSite['nodeNum'] = 0
                self.S.append(newSite)
                
        self.a = np.zeros((self.nodeNum, len(self.S)), np.uint8)
        for i in range(0, self.nodeNum):
            for j in range(0, len(self.S)):
                node = self.nodes.labelIndex[i]
                site = self.S[j]
                distance = sqrt(pow(node['x'] - site['x'], 2) + pow(node['y'] - site['y'], 2))
                if (distance < site['level']):
                    self.a[i][j] = 1
        #Update site mean and variance            
        for i in range(0, self.nodeNum):
            for j in range(0, len(self.S)):
                if (self.a[i][j] == 1):
                    self.S[j]['mean'] += self.nodes.labelIndex[i]['mean']
                    self.S[j]['nodeNum'] += 1
        for i in range(0, len(self.S)):
            if (self.S[i]['nodeNum'] != 0):
                self.S[i]['mean'] /= float(self.S[i]['nodeNum'])
        for i in range(0, self.nodeNum):
            for j in range(0, len(self.S)):
                self.S[j]['var'] += pow(self.nodes.labelIndex[i]['mean'] - self.S[j]['mean'], 2)
        for i in range(0, len(self.S)):
            if (self.S[i]['nodeNum'] != 0):
                self.S[i]['var'] /= float(self.S[i]['nodeNum'])
                self.S[i]['var'] = sqrt(self.S[i]['var'])
        
        self.w = np.zeros(self.nodeNum, np.float32)
        for i in range(0, len(self.w)):
            self.w[i] = self.nodes.labelIndex[i]['nodeNum']
            
        self.ca = np.zeros((self.nodeNum, len(self.S)), np.float32)
        for i in range(0, self.nodeNum):
            for j in range(0, len(self.S)):
                self.ca[i][j] = abs(self.nodes.labelIndex[i]['mean'] - self.S[j]['mean'])
        
        self.ce = np.zeros((self.nodeNum, len(self.S)), np.float32)
        for i in range(0, self.nodeNum):
            for j in range(0, len(self.S)):
                self.ce[i][j] = abs(self.nodes.labelIndex[i]['var'] - self.S[j]['var'])
                
        self.ci = np.zeros(len(self.S), np.float32)
        for i in range(0, len(self.S)):
            self.ci[i] =  abs(self.S[i]['level'] - self.currentLevel)
            
        self.z = np.zeros(len(self.S), np.uint8)
        self.x = np.zeros((self.nodeNum, len(self.S)), np.uint8)
        
    
    def heuristicSolve(self):
        minCost = 0.0
        self.updateParameters()
        #TODO: integer programming
        prob = cplex.Cplex()
        prob.objective.set_sense(prob.objective.sense.minimize)
        
        myObj = []
        myUb = []
        myLb = []
        myNames = []
        for i in range(0, len(self.ci)):
            tempVal = self.ci[i]
            for j in range(0, self.nodeNum):
                tempVal += (self.ca[j][i] + self.ce[j][i]) * self.w[j] * 1e-8
            myObj.append(tempVal)
            myUb.append(1)
            myLb.append(0)
            myNames.append(str(i))
        try:
            prob.variables.add(obj=myObj, ub=myUb, names=myNames)
        except Exception:
            print prob
        
        linExpr = []
        senses = []
        rhs = []
        for i in range(0, self.nodeNum):
            tempInd = []
            tempVal = []
            for j in range(0, len(self.S)):
                tempInd.append(j)
                tempVal.append(1)
            tempExpr = [tempInd, tempVal]
            linExpr.append(tempExpr)
            senses.append('G')
            rhs.append(1)
        prob.linear_constraints.add(lin_expr = linExpr, senses = senses, rhs = rhs)
        prob.solve()
        print('Solution status = ', prob.solution.get_status())
        # the following line prints the corresponding string
        print(prob.solution.status[prob.solution.get_status()])
        print("Solution value  = ", prob.solution.get_objective_value())
        
        return minCost

