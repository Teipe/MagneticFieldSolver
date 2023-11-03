import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

# Note the magnetic field starts from the top of the probe. Meaning if you want the field 1 mm under the probe, z = height + 1

radius  = 2e-3   #4 mm diameter
# radius  = 5e-4   #1 mm diameter
height  = 6e-3   #6 mm
loops   = 5
dz      = height/loops

#Constants
mu  = 1.257e-6  #m kg s**-2 A**-2
current =   1
pi = np.pi
k = mu*current/4/pi

startZ = 0e-3
endZ = 70e-3
numZ = 71
zArr = np.linspace(startZ, endZ, num=numZ)
# print(zArr)

startr = 0
endr = 4e-2
numr = 100
rArr = np.linspace(startr,  endr, num=numr)
numTheta = 100
theta1Arr = np.linspace(0, 2*pi, num=numTheta)
theta0Arr = np.linspace(0, loops*2*pi, num=100)

# Size of B = sizeOfZ * sizeOfTheta * sizeOfr
# File format <name>_<startZ>-<endZ>-<spaceZ>_<startr>-<endr>-<spacer>_<numTheta>.csv
B = []
for z in zArr:
    Bz = []
    for theta1 in theta1Arr:
        Br = []
        for r in rArr:
            d = np.sqrt((r*np.cos(theta1)-radius*np.cos(theta0Arr))**2+(r*np.sin(theta1)-radius*np.sin(theta0Arr))**2)
            z1 = z-dz*theta0Arr/2/pi 
            Br.append(k*np.trapz((radius*np.sin(np.arctan(z1/d)))/(np.sqrt(d**2+z1**2)**2)))
        Bz.append(Br)
    B.append(Bz)

B = np.array(B)
df = pd.DataFrame(B.flatten(), columns=['B'])
df.to_csv(f"magneticFieldR{radius}_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv")
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# # Create the mesh in polar coordinates and compute corresponding Z.
# r = np.linspace(0, 1.25, 50)
# p = np.linspace(0, 2*np.pi, 50)
# R, P = np.meshgrid(rArr, theta1Arr)
# B = np.array(B)

# # Express the mesh in the cartesian system.
# X, Y = R*np.cos(P), R*np.sin(P)

# # Plot the surface.
# ax.plot_surface(X, Y, B[3], cmap=plt.cm.YlGnBu_r)

# # Tweak the limits and add latex math labels.
# ax.set_zlim(np.amin(B[3]), np.amax(B[3]))
# ax.set_xlabel(r'$\phi_\mathrm{real}$')
# ax.set_ylabel(r'$\phi_\mathrm{im}$')
# ax.set_zlabel(r'$V(\phi)$')

# ax2 = fig.add_axes([0.1, 0.85, 0.8, 0.1])

# s = Slider(ax = ax2, label = 'value', valmin = 0, valmax = 100, valinit = 3, valstep=1)

# def update(val):
#     value = s.val
#     ax.cla()
#     ax.plot_surface(X, Y, B[value], cmap = plt.cm.YlGnBu_r)
#     ax.set_zlim(np.amin(B[value]), np.amax(B[value]))
#     # ax.set_zlim(-2, 7)

# s.on_changed(update)
# update(0)

# plt.show()