import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Loop position/size
radius = 3e-2/2 #d=3cm

startZ = 1e-3
endZ = 100e-3
numZ = 100

startr = 0
endr = 6e-3
numr = 100

numTheta = 100

zArr = np.linspace(startZ,  endZ, num=numZ)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

print('columnNames')
df = pd.read_csv(f"magneticField_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B = np.array(df.B)
B = B.reshape(numZ, numr, numTheta)

totalField = []

for i, z in enumerate(zArr):
    sumOfField = 0
    for j, r in enumerate(rArr):
        if r<=radius:
            for k, theta in enumerate(theta1Arr):
                sumOfField += B[i][j][k]
    totalField.append(sumOfField*(z**2))


plt.plot(zArr, totalField)
plt.show()