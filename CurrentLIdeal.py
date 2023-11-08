import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

xAxis = np.linspace(0, 40e-9, num=400)
# Assuming perfect square wave
# V = 100*[0]+300*[5]+100*[0]
# Using measured square wave
# Assuming ideal inductor
n = 5
l = 6e-3
radius = 2e-3
mu0  = 1.257e-6  #m kg s**-2 A**-2
mur = 30
#Magnetic permeability of metals is usually between 1500 to 3000
mu = mu0 * mur
ZL = n**2*radius**2*np.pi*mu/l
# ZL = ZL*2.5e-2
print(f'{ZL*1000} mH')
# ZL = 400e-9 # 0.4 uH
R = 1.8 # Ohm
Rloss = 2
C = 5e-12 # 5 pF
dt = 0.4e-9 #400 ps

# Loop position/size
rLoop = 3e-2/2 #d=3cm

startZ = 0e-3
endZ = 70e-3
numZ = 71

startr = 0
endr = 4e-2
numr = 100

numTheta = 100
dtTheta = 2*np.pi/numTheta

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)
dr = (endr-startr)/numr

# 4 for 4mm
df4 = pd.read_csv(f"magneticFieldR0.002_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B4 = np.array(df4.B)
B4 = B4.reshape(numZ, numr, numTheta)

sumOfField4 = 0
z = 6
# TODO: Account for dr and d0. Right now we only use them as point sources, but we need the integral, which contains dr
# from scipy.integrate import dblquad
# sumOfField4 = dblquad(lambda r, theta: B4[z], )
for j, r in enumerate(rArr):
    if r<=rLoop:
        for k, theta in enumerate(theta1Arr):
            sumOfField4 += B4[z][j][k]*dr*dtTheta*2*(r+dr)
sumOfField4 = sumOfField4

fig = plt.figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)

Iarr = []
EmfArr = []
relDiffPeak = []
for width in range(100, 550, 50):
  dfMeas = pd.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\WidthDependence\\raw_dumps\\150V\\width_{width}offset_0\\150_66.0,154.9,20_0.csv')
  Vtot = np.array(dfMeas['Channel A'])
  Etot = np.array(dfMeas['Channel C'])
  for i in range(1,10,1):
    dfMeas = pd.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\WidthDependence\\raw_dumps\\150V\\width_{width}offset_0\\150_66.0,154.9,20_{i}.csv')
    Vtot += np.array(dfMeas['Channel A'])
    Etot += np.array(dfMeas['Channel C'])

  V = Vtot/10
  V = V - np.average(V[0:60])
  Emeas = Etot/10
  VR = [] 
  # Voltage over inductor that opposes change in current
  VL = [0]
  VR = [0]
  # Current flowing through inductor
  I = []

  # Algorithm depends on last value, so have to do index 0 "manually"
  didt = VL[-1]/ZL
  Ic = C*V[0]/dt
  I.append(didt*dt)
  # VR = I[0]*R
  # VL = V[0]-VR
  VR.append((I[-1]+Ic)*Rloss+R)
  VL.append(VR[-1])

  for i, v in enumerate(V[1:]):
    didt = VL[-1]/ZL
    Ic = C*(v-V[i])/dt
    I.append(I[-1]+didt*dt)
    VR.append((I[-1]+Ic)*Rloss+R)
    VL.append(v-VR[-1])
  Iarr.append(I)
  EmfArr.append(sumOfField4*np.gradient(I))
  relDiffPeak.append(max(I)/max(EmfArr[-1]))


  # ax.plot(V, label=f'Input Voltage width: {width}')
  # # ax2.plot(I, 'orange', label='Inductor Current')
  # ax2.plot(np.gradient(I)-np.average(np.gradient(I)[0:400]), label=f'Emf width: {width}')
  # # ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Calculated Emf')
  # ax.legend(loc='upper left')
  # ax2.legend(loc='upper right')
  # ax = fig.add_subplot(122)
  # ax.plot(I, 'orange', label='Current through L')
  # ax.plot(Emeas, 'orange', label=f'Emf measured, width: {width}')
  # ax2.plot(I, 'orange', label='Inductor Current')
  ax.plot(I, label=f'Current theoretical, width: {width}')
  # ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Calculated Emf')
  ax.legend(loc='right')
  ax2.plot(VL, label=f'Voltage inductor theoretical, width: {width}')
  # ax2.plot(sumOfField4*np.gradient(I), 'orange', label='Calculated Emf')
  ax2.legend(loc='upper right')
  ax3.plot(V, label=f'Voltage, width: {width}')
  ax3.legend(loc='right')
  # ax2.legend(loc='upper right')


ax2 = fig.add_subplot(224)

for width in range(100, 500, 50):
  dfMeas = pd.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\WidthDependence\\raw_dumps\\150V\\width_{width}offset_0\\150_66.0,154.9,20_0.csv')
  V = dfMeas['Channel A']
  V = V - np.average(V[0:60])
  Emeas = dfMeas['Channel C']
  ax2.plot(Emeas, label=f'Emf measured width: {width}')
ax.legend()
ax2.legend()
plt.show()