import numpy as np 
import math as math
from numpy import linalg as lg
from classes import element as element
from classes import node as node
from classes import hflux as hflux
#from classes import SRspace as SRspace
from classes import constants
from classes import SR as SR

nodeFile = open("node.dat","r")
fluxbcFile = open("fluxbc.dat", "r")
powerDensityFile = open("powerDensity.dat", "w")
bcInfoFile = open("powerInfo.dat", "w")
nodes = {}
elements = {}
hfluxs = {}
elementInfo = []
connectivity = []
fluxbcInfo = []
fluxbcNode = []
fluxbcNodes = {}
aline = []
# read node geometry file
totalNode = 0
totalElement = 0
totalHfluxElement = 0

for line in nodeFile:
    aline = line.splitlines()
    nodeinfo = aline[0].split()
    inode = nodeinfo[0]
    x = nodeinfo[1]
    y = nodeinfo[2]
    z = nodeinfo[3]
    nodes[int(inode)] = node(inode,x,y,z)
    totalNode += 1

totalNode = inode
print("total node="+ str(inode))

# read element geometry file

# readElement()

# read flux boundary condition file
i = int(0)

totalPowerDeposit = 0.
totalArea = 0.
maxPowerDensity = 0.
maxProjectPowerDensity = 0.
maxIncidentAngle = 0.
maxx = 0.
maxy = 0.
maxz = 0.
maxmradx = 0.
maxmrady = 0.
mradx = 0.
mrady = 0.

class maxHeatLoadInfo(object): pass

#iterate each heat flux boundary surface element

for line in fluxbcFile:
    aline = line.splitlines()
    fluxbcInfo = aline[0].split()
# i,j,k are three vertex node number as surface number
    fluxSurfaceElement = fluxbcInfo[0]

    noList = ["5","6","7","9","10","12"]
    ijkList = ["i","j","k","l","m","n"]
# create node object by catching bc node number from input file
# map face nodal number into ijk for easy calculation
    for ijk, no in zip(ijkList, noList):
        fluxbcNodes[ijk] = nodes[int(fluxbcInfo[int(no)])]

# calculate power density and apply to individual node
    thisElementFlux = hflux(fluxbcNodes) 
    thisHeatLoadInfo = thisElementFlux.getHeatLoadInfo();
    totalArea += thisHeatLoadInfo["area"]

# only for print out coordinate
    centroidx = 1./3.* (fluxbcNodes["i"].x + fluxbcNodes["j"].x + fluxbcNodes["k"].x)
    centroidy = 1./3.* (fluxbcNodes["i"].y + fluxbcNodes["j"].y + fluxbcNodes["k"].y)
    centroidz = 1./3.* (fluxbcNodes["i"].z + fluxbcNodes["j"].z + fluxbcNodes["k"].z)

#   if(maxProjectPowerDensity <= thisHeatLoadInfo["projectPowerDensity"]):
    if(maxPowerDensity <= thisHeatLoadInfo["powerDensityInM"]):
        maxPowerDensity = thisHeatLoadInfo["powerDensityInM"]
        maxProjectPowerDensity = thisHeatLoadInfo["projectPowerDensity"]
        maxHeatLoadInfo = thisHeatLoadInfo
        maxIncidentAngle = thisHeatLoadInfo["incidentAngle"]*180./np.pi
        maxx = centroidx
        maxy = centroidy
        maxz = centroidz
        maxmradx = thisHeatLoadInfo["mradx"]
        maxmrady = thisHeatLoadInfo["mrady"]

    powerDensityFile.write(str(centroidx) + "," + str(centroidy) + "," + str(centroidz) + "," +\
                               str(thisHeatLoadInfo["projectPowerDensity"]) + "\n")
    mradx = thisHeatLoadInfo["mradx"]
    mrady = thisHeatLoadInfo["mrady"]
    bcInfoFile.write(str(mradx) + "," + str(mrady) + "," +\
                     str(thisHeatLoadInfo["powerDensityInMrad"]) + "," +\
                     str(thisHeatLoadInfo["powerDensityInM"]) + "," +\
                     str(thisHeatLoadInfo["incidentAngle"]*180./math.pi) + ", " +\
                     str(thisHeatLoadInfo["projectPowerDensity"]) + "\n")

    totalPowerDeposit += thisHeatLoadInfo["totalPower"]
    totalHfluxElement += 1

normalSR = SR(lg.norm(constants.target-constants.xLocal), 0.0, 0.0)
print("======================================================================\n")
print("on axis normal incident power density w/m^2= " + str(normalSR.powerDensityInM) + "\n")
print("total flux bc node =" + str(totalHfluxElement))
print("total area subjected to heat (m^2) =" + str(totalArea))
print("total power deposit (W)="  + str(totalPowerDeposit))

bcInfoFile.write("======================================================================\n")
bcInfoFile.write("on axis normal incident power density w/m^2= " + str(normalSR.powerDensityInM) + "\n")
bcInfoFile.write("total  node of flux bc=" + str(totalHfluxElement) + "\n")
bcInfoFile.write("max occuurs at (x,y,z) mm = " + str(maxx*1000.) + " , " + str(maxy*1000.) + " , " + str(maxz*1000.) + "\n" +\
                 "x mrad = " + str(maxmradx) + "  , y mrad = " + str(maxmrady) + "\n" +\
                 " max normal power density w/m^2 = " +\
                 str(maxPowerDensity) + " max projected Power density w/m^2 = " + str(maxProjectPowerDensity) +\
                 ", incident Angle = " + str(maxIncidentAngle) + " degree \n")
bcInfoFile.write("total flux bc node =" + str(totalHfluxElement) + " total area subjected to heat (mm^2) =" + \
                 str(totalArea*1000000) + " total power deposit (W)="  + str(totalPowerDeposit) + "\n" )

bcInfoFile.close()


def readElement():
    for line in elementFile:
        aline = line.splitlines()
        elementInfo = aline[0].split()
    if(len(elementInfo) > 2):
        ielement = elementInfo[10]
        connectivity  = elementInfo[11:19]
    if(len(elementInfo) == 2):
        connectivity.append(elementInfo[0])
        connectivity.append(elementInfo[1])
        elements[int(ielement)] = element(ielement, connectivity)
        totalElement += 1

    totalElement = len(elements)
    print("total element =" + str(totalElement))
