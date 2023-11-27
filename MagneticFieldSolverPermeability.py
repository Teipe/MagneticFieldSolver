import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Note the magnetic field starts from the top of the probe. Meaning if you want the field 1 mm under the probe, z = height + 1

radius  = 5e-3/2   #4 mm diameter
# radius  = 2e-3/2   #1 mm diameter
height  = 6e-3  #6 mm
loops   = 5
dz      = height/loops

#Constants
mu_0  = 1.257e-6  #m kg s**-2 A**-2
current =   1
pi = np.pi
k = mu_0*current/4/pi

#Ferrite properties
length = 6e-3
radius_fe = (radius*2-1e-3)/2
mu = 3000


startZ = 6.5e-3
endZ = 10.5e-3
numZ = 5
zArr = np.linspace(startZ, endZ, num=numZ)
# print(zArr)

startr = 0e-3
endr = 3e-2/2
numr = 100
rArr = np.linspace(startr,  endr, num=numr)
numTheta = 20
numTheta0 = 20
theta1Arr = np.linspace(0, 2*pi, num=numTheta)
theta0Arr = np.linspace(0, 2*pi*((numTheta0-1)/numTheta0), num=numTheta0)

Hn = []
Hs = []

startBar = 0e-3
endBar = 6e-3
numBar = 11
barArr = np.linspace(startBar, endBar, num=numBar)

dl = (2*radius*np.pi*loops)/numTheta0
for z in barArr:
    if z > length:
        break
    for theta1 in theta1Arr:
        Br = []
        for r in rArr:
            if r < radius_fe:
                point_source = 0
                for theta0 in theta0Arr:
                    for n in range(0,loops+1,1):
                        d = np.sqrt((r*np.cos(theta1)-radius*np.cos(theta0))**2+(r*np.sin(theta1)-radius*np.sin(theta0))**2)
                        z1 = z-n*height/loops
                        ### TODO: Radius here should be dl, which would be d(length of wire)
                        if d==0:
                            zComp = 0
                        else:
                            zComp=np.cos(np.arctan(z1/d))
                        if z1<0:
                            zComp = zComp*-1
                        cross=(np.pi/2-np.arccos(np.clip((radius**2+d**2-r**2)/(2*radius*d), -1, 1)))
                        point_source += k*zComp*((np.sin(cross))/np.sqrt(d**2+z1**2)**3)*dl
                    if point_source > 0:
                        Hn.append(point_source)
                    else:
                        Hs.append(point_source)   
            else: 
                break

print(f'H north: {mu*sum(Hn)/len(Hn)}')
print(f'H south: {mu*sum(Hs)/len(Hs)}')
# V is the ferromagnet volume
V = radius_fe**2*np.pi*length
#m = magnetic strength or magnetic dipole moment
m = mu*(abs(sum(Hn)/len(Hn))+abs(sum(Hs)/len(Hs)))/2*V/mu_0
print(f'V: {V}, V/u: {V/mu_0}')
print(f'm: {m}')
# Size of B = sizeOfZ * sizeOfTheta * sizeOfr
# File format <name>_<startZ>-<endZ>-<spaceZ>_<startr>-<endr>-<spacer>_<numTheta>.csv
B = []
Bperm = []
for z in zArr:
    Bz = []
    BpermZ = []
    for theta1 in theta1Arr:
        Br = []
        BpermR = []
        for r in rArr:
            BrTotal = 0
            for theta0 in theta0Arr:
                 for n in range(0,loops+1,1):
                    d = np.sqrt((r*np.cos(theta1)-radius*np.cos(theta0))**2+(r*np.sin(theta1)-radius*np.sin(theta0))**2)
                    z1 = z-n*height/loops# if r==0:
                    ### TODO: Radius here should be dl, which would be d(length of wire)
                    if d==0:
                        zComp = 0
                        cross=0
                    else:
                        zComp=np.cos(np.arctan(z1/d))
                        if z1<0:
                            zComp = zComp*-1
                        cross=(np.pi/2-np.arccos(np.clip((radius**2+d**2-r**2)/(2*radius*d), -1, 1)))
                    BrTotal += zComp*((np.sin(cross))/(d**2+z1**2))*dl
            # Bar magnet contribution:
            Bm = -m*((r**2+(z-height)**2)*np.cos(np.arctan(r/(z+height)))-(r**2+(z)**2)*np.cos(np.arctan(r/(z))))
            Bm=0
            Br.append(k*BrTotal)
            BpermR.append(k*BrTotal+Bm)
        Bz.append(Br)
        BpermZ.append(BpermR)
    B.append(Bz)
    Bperm.append(BpermZ)


# print(Bm)
# print(np.trapz((dl*np.sin(np.arctan(z1/d)))/(np.sqrt(d**2+z1**2)**2)))

# print(B[1][0])
# plt.figure()
# for i, theta in enumerate(theta1Arr):
#     plt.stem(i, B[1][i][numr-1])
# plt.show()

B = np.array(B)
Bperm = np.array(Bperm)
Bdict = {'B' : B.flatten(), 'Bperm' : Bperm.flatten()}
df = pd.DataFrame(Bdict)
df.to_csv(f"magneticFieldPermR{radius}_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv")