import numpy as np
import copy
from classes import constants

class node(object):
    def __init__(self,inode,x,y,z):
        self.inode = int(inode)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.coordinate = np.array([self.x, self.y, self.z])
        self.sourceCoordinate = self.coordinate - constants.source
        self.heatLoadCount = 0
        self.heatLoadInfos = []

    def getCoordinate():
        return self.coordinate

    def getSourceCoordinate():
        return self.sourceCoordinate

    def setNewCoordinate(self,newCoordinate):
        self.newCoordinate = newCoordinate

    def addHeatLoadInfo(self,surfaceElement, heatLoadInfo, localSurfaceID):
        self.heatLoadInfo = copy.deepcopy(heatLoadInfo)
        self.heatLoadInfo["localSurfaceID"] = localSurfaceID
        self.heatLoadInfo["surfaceElement"] = surfaceElement
        self.heatLoadInfos.append(self.heatLoadInfo)
        self.heatLoadCount = self.heatLoadCount + 1
        if(self.heatLoadCount > 1):
           print("add heatload on localid= " + localSurfaceID)