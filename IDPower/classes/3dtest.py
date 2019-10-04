import random
import numpy as np 
from numpy import linalg as lg


dFile = open("3d.dat","w")
nx = 200
ny = 200
data = 0.
dx = 1
dy = 1
x = 0.
y= 0.

for i in range(1,nx):
#    x = -50.+ dx*(i-1)
    for j in range(1, ny):
#        y = -50. + dy*(j-1)
        x = random.uniform(-0.1, 0.1)
        y = random.uniform(-0.1, 0.1)
        data = 100000*(x**2+y**2)
        print("x and y =" + str(x) + " , " +  str(y))
        dFile.write(str(x) + "\t" + str(y) + "\t" + "0." + "\t" + str(data) +"\n")

dFile.close()