import numpy as np
from skimage import segmentation
from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
import math

class CandidateSelector:
    def __init__(self, data):
        self.name = 'Candidate Selector'
        self.data = data
        self.candidates = []
    
    def GenerateKMeansCandidates(self, candNumber, disWeight):
        self.pixelLabelIndex = segmentation.slic(self.data, compactness=disWeight, n_segments=candNumber)
        self.reIndexLabels()
                
    def GenerateHierarchicalCandidates(self, candNumber):
        tempImg = np.reshape(self.data, (-1, 1))
        connectivity = grid_to_graph(*self.data.shape[:2])
        ward = AgglomerativeClustering(n_clusters=candNumber, linkage='ward', connectivity=connectivity).fit(tempImg)
        self.pixelLabelIndex = np.reshape(ward.labels_, self.data.shape[:2])
        self.reIndexLabels()
        
    def reIndexLabels(self):
        # Generate the candidate position index
        height, width = self.data.shape[:2]
        seqIndex = {}
        for h in range(0, height):
            for w in range(0, width):
                currentLabel = self.pixelLabelIndex[h, w]
                if (seqIndex.get(currentLabel) == None):
                    newLabelIndex = {}
                    newLabelIndex['x'] = w
                    newLabelIndex['y'] = h
                    newLabelIndex['nodeNum'] = 1
                    self.candidates.append(newLabelIndex)
                    seqIndex[currentLabel] = self.candidates.index(newLabelIndex)
                else:
                    tempIndex = seqIndex[currentLabel]
                    self.candidates[tempIndex]['x'] += w
                    self.candidates[tempIndex]['y'] += h
                    self.candidates[tempIndex]['nodeNum'] += 1
        for index in self.candidates:
            if (index['nodeNum'] != 0):
                index['x'] /= float(index['nodeNum'])
                index['y'] /= float(index['nodeNum'])