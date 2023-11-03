import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Loop position/size
radius = 3e-2/2 #d=3cm

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

print('columnNames')
df1 = pd.read_csv(f"magneticFieldR0.0005_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])
df4 = pd.read_csv(f"magneticFieldR0.002_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B1 = np.array(df1.B)
B4 = np.array(df4.B)
B1 = B1.reshape(numZ, numr, numTheta)
B4 = B4.reshape(numZ, numr, numTheta)

totalField1 = []
totalField4 = []

for i, z in enumerate(zArr):
    sumOfField1 = 0
    sumOfField4 = 0
    for j, r in enumerate(rArr):
        if r<=radius:
            for k, theta in enumerate(theta1Arr):
                sumOfField1 += B1[i][j][k]
                sumOfField4 += B4[i][j][k]
    totalField1.append(sumOfField1)
    totalField4.append(sumOfField4)

df2 = pd.read_csv(f"areaUnderPulse0-70-70.csv", usecols=['Area under pulse, flattened'])

data = np.array(df2['Area under pulse, flattened'])
data = data.reshape(4, 71)

dividedC1 = []
dividedC4 = []
for z in range(0,70):
    dividedC1.append(data[2][z]/totalField1[z+1])
    dividedC4.append(data[3][z]/totalField4[z+1])


fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()    
# plt.subplot(1, 2, 1)
plt.xlabel('z avstand [mm]')
plt.ylabel(r'Area Under Pulse')
ax.plot(data[2], label='Probe 1mm')
ax.plot(data[3], label='Probe 4mm')
# plt.legend()
# plt.subplot(1, 2, 2)
ax.set_xlabel('z avstand [mm]')
ax.set_ylabel(r'Area under pulse(Z)')
ax2.set_ylabel(r'Sum of magnetic field(Z)')
# plt.plot(range(0,71), to
# talField, label='Total Field')
# 6mm + 9mm/2 = 10.5 = 11
ax2.plot(totalField1[10:], 'green', label='Theoretical')
ax2.plot(totalField4[10:], 'green', label='Theoretical')
# plt.plot(range(1,71), dividedC4, label='Total Field')
# ax.legend()
ax.legend(loc='right') 
ax2.legend()
plt.show()