import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Loop position/size
radius = 3e-2/2 #d=3cm

offset = 1e-2
# offsetArr = np.linspace(0, 4e-2, num=5)
offsetThetaArr = np.linspace(0, 2*np.pi, num=5)

startZ = 6e-3
endZ = 16e-3
numZ = 11

startr = 0
endr = 4e-2
numr = 100
dr = (endr-startr)/numr

numTheta = 100
dtTheta = 2*np.pi/numTheta

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

# df1 = pd.read_csv(f"magneticFieldR0.0005_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])
df4 = pd.read_csv(f"magneticFieldR0.0025_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

# B1 = np.array(df1.B)
B4 = np.array(df4.B)
# B1 = B1.reshape(numZ, numr, numTheta)
B4 = B4.reshape(numZ, numTheta, numr)

# totalField1 = []
totalField4Offset = []

for offsetTheta in offsetThetaArr:
    if offsetTheta == 0:
        offsetThetaStep = 0
    else:
        print(offsetTheta)
        offsetThetaStep = int(offsetTheta/(2*np.pi)*numTheta)
    print(offsetThetaStep)
    totalField4z = []
    for i, z in enumerate(zArr):
        # sumOfField1 = 0
        sumOfField4Offset = 0
        for j, r in enumerate(rArr):
            if r<=radius:
                dA = ((2*dr+dr**2)*2*np.pi)/dtTheta
                for k, theta in enumerate(theta1Arr):
                    if offset - radius*np.cos(theta)<r*np.cos(theta) and radius*np.sin(theta)<r*np.sin(theta):
                        if k+offsetThetaStep > len(B4[i]):
                            sumOfField4Offset += B4[i][k-offsetThetaStep][j]
                        else:
                            sumOfField4Offset += B4[i][k+offsetThetaStep][j]
        totalField4z.append(sumOfField4Offset)
    totalField4Offset.append(totalField4z) 

fig = plt.figure()
ax = fig.add_subplot(111)
for i, offset in enumerate(offsetThetaArr):
    ax.plot(totalField4Offset[i], label=f'Theoretical Offset: {offset}')


ax.legend()
plt.show()