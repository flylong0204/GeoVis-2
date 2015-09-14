import numpy as np
import math
import cplex

class OverlayProcessor:
    def __init__(self, data, candPos, unValue):
        self.data = data
        self.candPos = candPos
        self.unValue = unValue
        self.levelNumber = len(unValue) - 1
        self.candNumber = len(candPos)
        self.alpha = 0.5
        self.beta = 0.5
        self.theta = 0.5
    
    def initParameters(self):
        #S: candidate sites
        #T: test nodes, which are all the data points in the grid
        #du: data uncertainty 
        #fu: feature uncertainty 
        #vu: visual uncertainty
        #z: if a glyph is positioned
        
        # update site info
        self.S = []
        for i in range(1, self.levelNumber + 1):
            for j in range(len(self.unValue[i])):
                tempS = {}
                tempS['x'] = self.candPos[j]['x']
                tempS['y'] = self.candPos[j]['y']
                tempS['level'] = i
                self.S.append(tempS)
                
        # update data uncertainty
        self.du = []
        for i in range(1, self.levelNumber + 1):
            for j in range(len(self.unValue[i])):
                tempDu = {}
                tempDu['mean'] = self.unValue[i][j]['mean']
                tempDu['var'] = self.unValue[i][j]['var']
                self.du.append(tempDu)
        
        # update feature uncertainty
        self.acc = np.zeros((self.candNumber, len(self.du)), np.int8)
        for i in range(self.candNumber):
            for j in range(len(self.S)):
                cand = self.candPos[i]
                site = self.S[j]
                distance = math.sqrt(pow(cand['x'] - site['x'], 2) + pow(cand['y'] - site['y'], 2))
                if (distance < pow(2, site['level']) / 2):
                    self.acc[i][j] = 1
                    
        self.fu = []
        for i in range(len(self.S)):
            tempDict = {}
            tempDict['mean'] = 0
            tempDict['var'] = 0
            tempDict['fnum'] = 0
            self.fu.append(tempDict)
        for i in range(self.candNumber):
            for j in range(len(self.S)):
                if (self.acc[i][j] == 1):
                    self.fu[j]['mean'] += self.du[j]['mean']
                    self.fu[j]['fnum'] += 1
        for i in range(len(self.S)):
            if (self.fu[i]['fnum'] != 0):
                self.fu[i]['mean'] /= self.fu[i]['fnum']
        for i in range(self.candNumber):
            for j in range(len(self.S)):
                if (self.acc[i][j] == 1):
                    self.fu[j]['var'] += pow(self.du[i]['mean'] - self.fu[j]['mean'], 2)
        for i in range(len(self.S)):
            if (self.fu[i]['fnum'] != 0):
                self.fu[i]['var'] = math.sqrt(self.fu[i]['var'] / self.fu[i]['fnum'])
    
    def setCurrentLevel(self, level):
        self.currentLevel = level
        
    def setParameters(self, a, b, c):
        self.alpha = a
        self.beta = b 
        self.theta = c
        self.initParameters()
    
    def updateParameters(self):
        # update visual uncertainty
        self.vu = np.zeros(len(self.S), np.float32)
        for i in range(0, len(self.S)):
            if self.S[i]['level'] < self.currentLevel:
                self.vu[i] = math.exp(-1 * (self.S[i]['level'] - self.currentLevel))
            else:
                self.vu[i] = math.exp(2 * (self.S[i]['level'] - self.currentLevel))
        
    
    def heuristicSolve(self, level):
        self.currentLevel = level
        self.updateParameters()
        
        prob = cplex.Cplex()
        prob.objective.set_sense(prob.objective.sense.minimize)
        
        myObj = []
        myUb = []
        myLb = []
        myNames = []
        for i in range(0, len(self.S)):
            zPara = 0
            zPara = self.du[i]['var'] * self.alpha + self.fu[i]['var'] * self.beta + self.vu[i] * self.theta
            print ("du: " + str(self.du[i]['var']) + "   fu: " + str(self.fu[i]['var']) + "   vu:" + str(self.vu[i]) + "\n")
            myObj.append(float(zPara))
            myUb.append(1)
            myLb.append(0)
            myNames.append(str(i))
        try:
            prob.variables.add(obj=myObj, lb=myLb, ub=myUb, types=[prob.variables.type.binary] * len(self.S), names=myNames)
        except Exception as ex:
            print ex
        
        linExpr = []
        senses = []
        rhs = []
        for i in range(0, self.candNumber):
            tempInd = []
            tempVal = []
            for j in range(0, len(self.S)):
                tempInd.append(j)
                tempVal.append(1 * self.acc[i][j])
            tempExpr = [tempInd, tempVal]
            linExpr.append(tempExpr)
            senses.append('E')
            rhs.append(1)
        prob.linear_constraints.add(lin_expr = linExpr, senses = senses, rhs = rhs)
        prob.solve()
        #print('Solution status = ', prob.solution.get_status())
        # the following line prints the corresponding string
        #print(prob.solution.status[prob.solution.get_status()])
        #print("Solution value  = ", prob.solution.get_objective_value())
        
        #numcols = prob.variables.get_num()
        #pi = prob.solution.get_dual_values()
        self.z = prob.solution.get_values()
#         dj = prob.solution.get_reduced_costs()
#         for i in range(numrows):
#             print("Row %d:  Slack = %10f  Pi = %10f" % (i, slack[i], pi[i]))
#         for j in range(numcols):
#             print("Column %d:  Value = %10f Reduced cost = %10f" %
#                   (j, self.z[j], dj[j]))
        #for j in range(numcols):
            #print("Column %d:  Value = %10f" % (j, self.z[j]))
        
        return self.z
    
    def heuristicSolveWeight(self, level, weights):
        self.currentLevel = level
        self.updateParameters()
        
        prob = cplex.Cplex()
        prob.objective.set_sense(prob.objective.sense.minimize)
        
        myObj = []
        myUb = []
        myLb = []
        myNames = []
        for i in range(0, len(self.S)):
            zPara = 0
            zPara = (self.du[i]['var'] * self.alpha + self.fu[i]['var'] * self.beta + self.vu[i] * self.theta) * (1.0 - weights[i])
            print ("du: " + str(self.du[i]['var']) + "   fu: " + str(self.fu[i]['var']) + "   vu:" + str(self.vu[i]) + "\n")
            myObj.append(float(zPara))
            myUb.append(1)
            myLb.append(0)
            myNames.append(str(i))
        try:
            prob.variables.add(obj=myObj, lb=myLb, ub=myUb, types=[prob.variables.type.binary] * len(self.S), names=myNames)
        except Exception as ex:
            print ex
        
        linExpr = []
        senses = []
        rhs = []
        for i in range(0, self.candNumber):
            tempInd = []
            tempVal = []
            for j in range(0, len(self.S)):
                tempInd.append(j)
                tempVal.append(1 * self.acc[i][j])
            tempExpr = [tempInd, tempVal]
            linExpr.append(tempExpr)
            senses.append('E')
            rhs.append(1)
        prob.linear_constraints.add(lin_expr = linExpr, senses = senses, rhs = rhs)
        prob.solve()
        self.z = prob.solution.get_values()
        return self.z

