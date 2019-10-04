import numpy as np 
import math as math
from numpy import linalg as lg

#electron energy (GeV)
GeV = 2.

#current (mA)
beamCurrent = 500

# period length lambda [cm]
lambda0 = 1.9

# number of period N
N = 208

# By magnet field T [tesla)
magnetBy = 1.126959

# Bx magnet field T (tesla)
magnetBx = 0.0

# total length of ID (m)
totalLength = lambda0*N/100.

# deflection parameter Ky
Ky = 0.934 * lambda0 * magnetBy

# deflection parameter Kx
Kx = 0.934 * lambda0 * magnetBx

# gamma 1/mrad
gamma = 1957.*GeV/1000.