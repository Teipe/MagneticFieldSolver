import numpy as np
import matplotlib.pyplot as plt

endTime = 400e-9
nSamples = 800
tAxis = np.linspace(0, endTime, num=nSamples)
# Assuming perfect square wave
# V = 100*[0]+300*[5]+100*[0]
# Using measured square wave
# Assuming ideal inductor
n = 5
l = 6e-3
radius = 2e-3
mu0  = 1.257e-6  #m kg s**-2 A**-2
mur = 30000
#Magnetic permeability of metals is usually between 1500 to 3000
mu = mu0 * mur
ZL = n**2*radius**2*np.pi*mu/l
# ZL = ZL*2.5e-2
print(f'{ZL*1000} mH')
# ZL = 400e-9 # 0.4 uH
R = 1.8 # Ohm
# Rloss = 2
# C = 5e-12 # 5 pF
dt = endTime/nSamples

Cbat = 5e-6 #5 uF
# Rise time of the supply, dependent on the transistor switch
Vc0 = 150   #[V]

# Pulse shape
tau = 5e-9  #5 ns
width = 100e-9 #100 ns

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

fig = plt.figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

VcArr = [Vc0]

# Voltage over inductor that opposes change in current
VL = [0]
VR = [0]
# Current flowing through inductor
I = [0]
Vsupply = []


for i, t in enumerate(tAxis[:205]):
    if t<width/2:
        Vsupply.append(VcArr[-1]*(1-np.e**(-t/tau)))
    else:   
        Vsupply.append(VcArr[-1]*(1-(1/(np.e**(-(t-width-tau)/tau)))))
        print(f'{i}={t}:         {1-(1/(np.e**(-(t-width-tau)/tau)))}')
    # Algorithm depends on last value, so have to do index 0 "manually"
    didt = VL[-1]/ZL
    # Ic = C*VcArr[0]/dt
    I.append(didt*dt)
    # VR = I[0]*R
    # VL = V[0]-VR
    # VR.append((I[-1]+Ic)*Rloss+R)
    VR.append((I[-1])+R)
    VL.append(Vsupply[-1]-VR[-1])
    # VcArr.append(VcArr[-1]-(I[-1]+Ic)*dt)
    VcArr.append(VcArr[-1]-(I[-1])*dt)
    

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
ax3.plot(Vsupply, label=f'Voltage supply, width: {width}')
ax3.legend(loc='right')
ax4.plot(VcArr, label=f'Voltage Capacitor bank, width: {width}')
ax4.legend(loc='right')
# ax2.legend(loc='upper right')

plt.show()