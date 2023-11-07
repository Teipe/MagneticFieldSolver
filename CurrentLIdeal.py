import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

xAxis = np.linspace(0, 40e-9, num=400)
# Assuming perfect square wave
# V = 100*[0]+300*[5]+100*[0]
# Using measured square wave
dfMeas = pd.read_csv(f"150_66.0,154.9,7.5_0.csv", usecols=['Channel A', 'Channel C'])
V = dfMeas['Channel A']
Emeas = dfMeas['Channel C']
# Assuming ideal inductor
n = 5
l = 6e-3
radius = 2e-3
mu0  = 1.257e-6  #m kg s**-2 A**-2
mur = 1500
#Magnetic permeability of metals is usually between 1500 to 3000
mu = mu0 * mur
ZL = n**2*radius**2*np.pi*mu/l
# ZL = ZL*2.5e-2
print(f'{ZL*1000} mH')
# ZL = 400e-9 # 0.4 uH
R = 1.8 # Ohm
dt = 0.4e-9 #400 ps

# Voltage over inductor that opposes change in current
VL = [0]
# Current flowing through inductor
I = []

# Algorithm depends on last value, so have to do index 0 "manually"
didt = VL[-1]/ZL
I.append(didt*dt)
# VR = I[0]*R
# VL = V[0]-VR

for i, v in enumerate(V[1:]):
  VR = I[-1]*R
  VL.append(v-VR)
  didt = VL[-1]/ZL
  I.append(I[-1]+didt*dt)

# Loop position/size
rLoop = 3e-2/2 #d=3cm

startZ = 0e-3
endZ = 70e-3
numZ = 71

startr = 0
endr = 4e-2
numr = 100

numTheta = 100

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

df4 = pd.read_csv(f"magneticFieldR0.002_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B4 = np.array(df4.B)
B4 = B4.reshape(numZ, numr, numTheta)


sumOfField4 = 0
z = 6
for j, r in enumerate(rArr):
    if r<=rLoop:
        for k, theta in enumerate(theta1Arr):
            sumOfField4 += B4[z][j][k]
sumOfField4 = sumOfField4*mur
print(sumOfField4)

fig = plt.figure()
ax = fig.add_subplot(121)
# ax.plot(I, 'orange', label='Current through L')
ax2 = ax.twinx()
ax.plot(V, label='Input Voltage')
# ax2.plot(I, 'orange', label='Inductor Current')
ax2.plot(np.gradient(I)-np.average(np.gradient(I)[0:400]), 'orange', label='Emf')
# ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Calculated Emf')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax = fig.add_subplot(122)
# ax.plot(I, 'orange', label='Current through L')
ax2 = ax.twinx()
ax.plot(Emeas, label='Emf measured')
# ax2.plot(I, 'orange', label='Inductor Current')
ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Emf')
# ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Calculated Emf')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.show()