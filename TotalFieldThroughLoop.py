import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Loop position/size
radius = 3e-2/2 #d=3cm
radius1 = 1e-2/2 #d=3cm

startZ = 6e-3
endZ = 26e-3
numZ = 201

startr = 0
endr = 1e-2
numr = 200

numTheta = 100
dtTheta = 2*np.pi/numTheta
dr = (endr-startr)/numr

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

df1 = pd.read_csv(f"magneticFieldR0.001_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])
df4 = pd.read_csv(f"magneticFieldR0.0025_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B1 = np.array(df1.B)
B4 = np.array(df4.B)
B1 = B1.reshape(numZ, numTheta, numr)
B4 = B4.reshape(numZ, numTheta, numr)

totalField1 = []
totalField4 = []
totalField1_1 = []
totalField4_1 = []

for i, z in enumerate(zArr[5:]):
    sumOfField1 = 0
    sumOfField4 = 0
    sumOfField1_1 = 0
    sumOfField4_1 = 0
    for j, r in enumerate(rArr):
        if r<=radius1:
            ### 2dr + dr^2 is a simplifaction of (r+dr)^2-r^2
            dA = ((2*dr+dr**2)*2*np.pi)/dtTheta
            for k, theta in enumerate(theta1Arr):
                sumOfField1 += B1[i][k][j]*dA
                sumOfField4 += B4[i][k][j]*dA
                sumOfField1_1 += B1[i][k][j]*dA
                sumOfField4_1 += B4[i][k][j]*dA
        elif r<=radius:
            dA = ((2*dr+dr**2)*2*np.pi)/dtTheta
            for k, theta in enumerate(theta1Arr):
                sumOfField1 += B1[i][k][j]*dA
                sumOfField4 += B4[i][k][j]*dA
    totalField1.append(sumOfField1)
    totalField4.append(sumOfField4)
    totalField1_1.append(sumOfField1_1)
    totalField4_1.append(sumOfField4_1)

# df2 = pd.read_csv(f"areaUnderPulse0-70-70.csv", usecols=['Area under pulse, flattened'])

# data = np.array(df2['Area under pulse, flattened'])
# data = data.reshape(4, 71)

# dividedC1 = []
# dividedC4 = []
# for z in range(0,70):
#     dividedC1.append(data[2][z]/totalField1[z+1])
#     dividedC4.append(data[3][z]/totalField4[z+1])


fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()
# plt.subplot(1, 2, 1)
# ax.plot(data[2], label='Probe 1mm')
# ax.plot(data[3], label='Probe 4mm')
# plt.legend()
# plt.subplot(1, 2, 2)
ax.set_xlabel('z avstand [mm]')
ax.set_ylabel(r'Sum of $B_Z$ through loop [T/A]')
# ax2.set_ylabel(r'Sum of magnetic field(Z)')
# plt.plot(range(0,71), to
# talField, label='Total Field')
# 6mm + 9mm/2 = 10.5 = 11
ax.plot(zArr[5:]*1000-6, totalField1, label='1mm 3cm loop')
ax.plot(zArr[5:]*1000-6, totalField1_1, label='1mm 1cm loop')
ax.plot(zArr[5:]*1000-6, totalField4, label='4mm 3cm loop')
ax.plot(zArr[5:]*1000-6, totalField4_1, label='4mm 1cm loop')
# ax2.plot(zArr*1000-6, totalField4[0]/((zArr)**2))
# plt.plot(range(1,71), dividedC4, label='Total Field')
# ax.legend()
ax.legend(loc='right') 
plt.show()