import numpy as np 
import math as math
from numpy import linalg as lg

#setup in mm not meter
# source = np.array([0,0,8500],dtype=float)
# xLocal = np.array([4.42 ,-0.06 ,8500],dtype=float)

# for slit offset 4mm x 4mm
#source = np.array([4,-4,8500],dtype=float)
#xLocal = np.array([8.37 ,-4.11 ,8500],dtype=float)
#target = np.array([3.95, -4.03, 17.62],dtype=float)

# for premask offset
source = np.array([3.95,5.95,8000.],dtype=float)
xLocal = np.array([8.11 ,5.89 ,8000],dtype=float)
target = np.array([3.95,-4.03,17.62],dtype=float)

# for test plate
#source = np.array([0.,0.,8000],dtype=float)
#xLocal = np.array([1.,0. ,8000],dtype=float)
#target = np.array([0.,0.,0.],dtype=float)

#convert to meter which is used in ANSYS
source *= 1.e-03
xLocal *= 1.e-03
target *= 1.e-03

#tolerance of finding incident angle
epsilon = 1.e-10

nx = np.subtract(xLocal,source)
nz = np.subtract(target,source)
ny = np.cross(nx, nz)

print("innder product = " + str(np.inner(nx,ny)))
print("innder product = " + str(np.inner(ny,nz)))
print("innder product = " + str(np.inner(nx,nz)))

nx /= lg.norm(nx)
ny /= lg.norm(ny)
nz /= lg.norm(nz)
print("here")