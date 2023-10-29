import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

startZ = 1e-3
endZ = 20e-3
numZ = 20

startr = 0
endr = 20e-3
numr = 100

numTheta = 100

rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

print('columnNames')
df = pd.read_csv(f"magneticField_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B = np.array(df.B)
B = B.reshape(numZ, numr, numTheta)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Create the mesh in polar coordinates and compute corresponding Z.
R, P = np.meshgrid(rArr, theta1Arr)
B = np.array(B)

# Express the mesh in the cartesian system.
X, Y = R*np.cos(P), R*np.sin(P)

# Plot the surface.
ax.plot_surface(X, Y, B[3], cmap=plt.cm.YlGnBu_r)

# Tweak the limits and add latex math labels.
ax.set_zlim(np.amin(B[3]), np.amax(B[3]))
ax.set_xlabel(r'$\phi_\mathrm{real}$')
ax.set_ylabel(r'$\phi_\mathrm{im}$')
ax.set_zlabel(r'$V(\phi)$')

ax2 = fig.add_axes([0.1, 0.85, 0.8, 0.1])

s = Slider(ax = ax2, label = 'value', valmin = 0, valmax = numZ-1, valinit = 3, valstep=1)

def update(val):
    value = s.val
    ax.cla()
    ax.plot_surface(X, Y, B[value], cmap = plt.cm.YlGnBu_r)
    ax.set_zlim(np.amin(B[value]), np.amax(B[value]))
    # ax.set_zlim(-2, 7)

s.on_changed(update)
update(0)

plt.show()