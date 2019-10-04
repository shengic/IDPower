import math as math
import numpy as np
from numpy import linalg as lg
from classes import SRconstants
from classes import constants
from scipy import integrate

class SR(object):
   
   def __init__(self, distance, thetax, thetay):
    self.distance = distance
    self.thetax = thetax
    self.thetay = thetay
#uncomment thetax and thetay out to check normal on-axis power density
#    self.thetax = 0.
#    self.thetay = 0.
    self.totalPower = self.getTotalPower()
    self.powerDensityInMrad = self.getPowerDensityInMrad()
#input is in meter convert from kW/mrad^2 to W/m^2 is to multiple 10^9
    self.powerDensityInM = self.powerDensityInMrad*1.e09/math.pow(self.distance,2)
    print("powerDensity in w/meter^2= " + str(self.powerDensityInM))

   def getPowerDensityInMrad(self):
    f = lambda alpha : \
        (math.pow(SRconstants.Ky*math.cos(alpha),2) + \
         math.pow(SRconstants.Kx*math.sin(alpha),2))/ \
         math.pow(1.+ math.pow(SRconstants.Ky*math.sin(alpha)- SRconstants.gamma*self.thetax,2) +\
         math.pow(SRconstants.Kx*math.cos(alpha)-SRconstants.gamma*self.thetay,2),3) - \
         \
         math.pow((math.pow(SRconstants.Ky,2)-math.pow(SRconstants.Kx,2))*math.sin(2.*alpha)- \
         2.*SRconstants.Ky*SRconstants.gamma*self.thetax*math.cos(alpha)+ \
         2.*SRconstants.Kx*SRconstants.gamma*self.thetay*math.sin(alpha),2)/ \
         math.pow(1.+ math.pow(SRconstants.Ky*math.sin(alpha)- SRconstants.gamma*self.thetax,2) +\
         math.pow(SRconstants.Kx*math.cos(alpha)-SRconstants.gamma*self.thetay,2),5)

    result, err = integrate.quad(f, -math.pi, math.pi)

    self.powerDensityInMrad = 0.0844*math.pow(SRconstants.GeV,4)*SRconstants.beamCurrent/1000.*SRconstants.totalLength/ \
                              math.pow(SRconstants.lambda0/100.,2)*result
# W convert to kW
    self.powerDensityInMrad /= 1000.
#    print("power density kW/mrad^2 = " + str(self.powerDensityInMrad))
    return self.powerDensityInMrad

   def getPowerDensityInM(self):
      return self.powerDensityInM;

   def gfunction(self, alpha):
     self.D = 1.+ math.pow(SRconstants.Ky*math.sin(alpha)- SRconstants.gamma*self.thetax,2) +\
         math.pow(SRconstants.Kx*math.cos(alpha)-SRconstants.gamma*self.thetay,2)
     self.gfunction = (math.pow(SRconstants.Ky*math.cos(alpha),2) + \
                       math.pow(SRconstants.Kx*math.sin(alpha),2))/ \
                       math.pow(self.D,3) - \
         math.pow((math.pow(SRconstants.Ky,2)-math.pow(SRconstants.Kx,2))*math.sin(2.*alpha)- \
         2.*SRconstants.Ky*SRconstants.gamma*self.thetax*math.cos(alpha)+ \
         2.*SRconstants.Kx*SRconstants.gamma*self.thetay*math.sin(alpha),2)/ \
         math.pow(self.D,5)
     return self.gfunction

   def getTotalPower(self):
    self.totalPower = 0.633*SRconstants.GeV* \
        (math.pow(SRconstants.magnetBx,2.)+math.pow(SRconstants.magnetBy,2.))* \
        SRconstants.totalLength*SRconstants.beamCurrent
    return self.totalPower

