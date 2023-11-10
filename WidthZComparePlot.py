import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

xAxis = np.linspace(0, 599.4e-9, num=999)
# Assuming perfect square wave
# V = 100*[0]+300*[5]+100*[0]
# Using measured square wave
# Assuming ideal inductor
n = 5
l = 6e-3
radius1 = 0.5e-3
radius = 2e-3
mu0  = 1.257e-6  #m kg s**-2 A**-2
mur = 1
#Magnetic permeability of metals is usually between 1500 to 3000
mu = mu0 * mur
ZL = n**2*radius**2*np.pi*mu/l
ZL1 = n**2*radius1**2*np.pi*mu/l
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

# Z of printer
startZPrint = 14
endZPrint = 30
dZ = 2
zPrintArr = range(startZPrint, endZPrint+dZ, dZ)

startr = 0
endr = 4e-2
numr = 100

numTheta = 100
dtTheta = 2*np.pi/numTheta

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)
dr = (endr-startr)/numr

Iarr = []
EmfArr = []
relDiffPeak = []

measFolder = f'WidthZDependence1mm'

EmeasArr = []
VmeasArr = []
VoverE = [[],[],[],[],[],[],[],[],[]]

for z in zPrintArr:
  EmeasWArr = []
  VmeasWArr = []
  for n, width in enumerate(range(100, 550, 50)):
    dfMeas = pd.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\{measFolder}\\raw_dumps\\150V\\width_{width}offset_0\\150_66.0,154.9,{z}_0.csv')
    Vtot = np.array(dfMeas['Channel A'])
    Etot = np.array(dfMeas['Channel C'])
    for i in range(1,10,1):
      dfMeas = pd.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\{measFolder}\\raw_dumps\\150V\\width_{width}offset_0\\150_66.0,154.9,{z}_{i}.csv')
      Vtot += np.array(dfMeas['Channel A'])
      Etot += np.array(dfMeas['Channel C'])

    V = Vtot/10
    V = V - np.average(V[0:60])
    Emeas = Etot/10

    EmeasWArr.append(Emeas)
    VmeasWArr.append(V)
    VoverE[n].append(np.trapz(Emeas)/np.trapz(V))

    # VR = [] 
    # # Voltage over inductor that opposes change in current
    # VL = [0]
    # VR = [0]
    # # Current flowing through inductor
    # I = []

    # # Algorithm depends on last value, so have to do index 0 "manually"
    # didt = VL[-1]/ZL
    # Ic = C*V[0]/dt
    # I.append(didt*dt)
    # # VR = I[0]*R
    # # VL = V[0]-VR
    # VR.append((I[-1]+Ic)*Rloss+R)
    # VL.append(VR[-1])

    # for i, v in enumerate(V[1:]):
    #   didt = VL[-1]/ZL
    #   Ic = C*(v-V[i])/dt
    #   I.append(I[-1]+didt*dt)
    #   VR.append((I[-1]+Ic)*Rloss+R)
    #   VL.append(v-VR[-1])
    # Iarr.append(I)
    # EmfArr.append(np.gradient(I))
    # relDiffPeak.append(max(I)/max(EmfArr[-1]))

  EmeasArr.append(EmeasWArr)
  VmeasArr.append(VmeasWArr)

fig = plt.figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


for n, width in enumerate(range(100, 550, 50)):
  ax4.plot(VoverE[n], label=f'Width: {width}')
ax4.legend()

ax5 = fig.add_axes([0.1, 0.85, 0.8, 0.1])

s = Slider(ax = ax5, label = 'value', valmin = 0, valmax = len(zPrintArr)-1, valinit = 3, valstep=1)

def update(val):
    value = s.val
    ax.cla()
    ax2.cla()
    ax3.cla()
    for width in range(0, 9, 1):
      ax.plot(EmeasArr[value][width], label=f'{width}: Emf measured')
      ax2.plot(VmeasArr[value][width], label=f'{width}: Voltage measured')
      ax3.stem(width, np.trapz(VmeasArr[value][width])/np.trapz(EmeasArr[value][width]), label=f'V/Emf, width: {width}')

    # ax.set_zlim(-2, 7)

s.on_changed(update)
update(0)
ax.legend()
ax2.legend()
plt.show()
