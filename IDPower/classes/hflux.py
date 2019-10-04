import numpy as np
import math as math
from classes import constants
from classes.SR import SR as SR
from classes import node as node
from numpy import linalg as lg
import sys, traceback

class hflux(object):
    def __init__(self, bcnodeObj):
        global source, target, xLocal, nx,ny,nz
        self.surfaceNodes = bcnodeObj
# get vector ij x ik to determine triangle area
        self.vectorIJ = bcnodeObj["j"].sourceCoordinate-bcnodeObj["i"].sourceCoordinate
        self.vectorIK = bcnodeObj["k"].sourceCoordinate-bcnodeObj["i"].sourceCoordinate
        self.cross = np.cross(self.vectorIJ, self.vectorIK)
        self.area = 0.5*lg.norm(self.cross)
        self.normal = self.cross/lg.norm(self.cross)
#        print("the area is " + str(self.area))
# convert to new coordinate to calculate thetax and thetay
        for index in bcnodeObj:
# set coordinate based on on-axis beam vector
            self.surfaceNodes[index].setNewCoordinate(self.convertNewCoordinate(bcnodeObj[index]))
 
        self.vectorFromSource = 1./3.*(self.surfaceNodes["i"].sourceCoordinate + 
                                       self.surfaceNodes["j"].sourceCoordinate +
                                       self.surfaceNodes["k"].sourceCoordinate)
        self.centroidCoordinate = 1./3.*(self.surfaceNodes["i"].newCoordinate + 
                                         self.surfaceNodes["j"].newCoordinate +
                                         self.surfaceNodes["k"].newCoordinate)

        self.distanceFromSource = lg.norm(self.vectorFromSource)
        self.unitVectorFromSource = self.vectorFromSource/self.distanceFromSource
        self.incidentAngle = self.findIncidentAngle()
        self.thetax = np.arctan(self.centroidCoordinate[0]/self.centroidCoordinate[2])*1000.
        self.thetay = np.arctan(self.centroidCoordinate[1]/self.centroidCoordinate[2])*1000.
        self.SR = SR(self.distanceFromSource, self.thetax, self.thetay)
        self.powerDensityInMrad = self.SR.getPowerDensityInMrad()
        self.powerDensityInM = self.SR.getPowerDensityInM()
        self.projectPowerDensity = self.powerDensityInM * math.sin(self.incidentAngle)
#        self.projectPowerDensity = self.powerDensityInM 
        self.totalPower = self.area * self.projectPowerDensity
        self.heatLoadInfo = {"area" : self.area, \
                             "distance" : self.distanceFromSource, \
                             "mradx" : self.thetax,\
                             "mrady" : self.thetay, \
                             "powerDensityInMrad" : self.powerDensityInMrad, \
                             "powerDensityInM" : self.powerDensityInM, \
                             "totalPower": self.totalPower, \
                             "incidentAngle" : self.incidentAngle, \
                             "projectPowerDensity" : self.projectPowerDensity
                             }
        print("here")

    def getHeatLoadInfo(self):
        return self.heatLoadInfo

    def getSurfaceArea(bcnodeObj):
        return self.area

    def getPowerDensityInMrad(self):
        return self.powerDensityInMrad

    def getPowerDensityInM(self):
        return self.powerDensityInM;

    def getTotalPower(self):
        return self.totalPower

    def getIncidentAngle(self):
        return self.incidentAngle

    def getSurfaceNodes(self):
        return self.surfaceNodes

    def getHeatLoadInfo(self):
        return self.heatLoadInfo

    def findIncidentAngle(self):
        self.incidentAngle =  np.arccos(np.dot(self.vectorFromSource, self.normal)/
        (lg.norm(self.vectorFromSource)*lg.norm(self.normal)))
        if(self.incidentAngle > np.pi/2):
            self.incidentAngle -= np.pi/2.
        else:
            self.incidentAngle = np.pi/2. - self.incidentAngle

        if(np.abs(self.incidentAngle) <= constants.epsilon):
            self.incidentAngle = 0.0
        if(self.incidentAngle < 0.0):
            print("incident angle is less than 0= " + str(self.incidentAngle))
            self.incidentAngle = 0.0
            sys.exit(1)
        print("incident angle = " + str(np.rad2deg(self.incidentAngle))+ " degree")
        return self.incidentAngle

    def getNormal():
        return self.normal

    def convertNewCoordinate(self, thisNode):
        a = np.transpose(np.array([constants.nx, constants.ny, constants.nz]))
        b = thisNode.sourceCoordinate
        x = np.linalg.solve(a,b)
        return x