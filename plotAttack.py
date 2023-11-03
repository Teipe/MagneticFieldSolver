import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

df = pd.read_csv(f"all_attacks.csv")

B = np.array(df['Peak Voltage Probe'])
avgB = []
for i in range(0,31*31):
  Bi = 0
  for n in range(0,10):
    Bi += B[i*n+n]
  avgB.append(Bi/10)
avgB = np.array(avgB).reshape(31, 31)
    

# plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Create the mesh in polar coordinates and compute corresponding Z.
X, Y = np.meshgrid(np.linspace(0, 30, num=31), np.linspace(0, 30, num=31))
B = np.array(avgB)

# Express the mesh in the cartesian system.
# X, Y = R*np.cos(P), R*np.sin(P)

# Tweak the limits and add latex math labels.
ax.set_zlim(np.amin(B), np.amax(B))
ax.set_xlabel(f'1/R')
ax.set_ylabel(r'1/R')
ax.set_zlabel(r'Bz')
# Plot the surface.
ax.plot_surface(X, Y, B, cmap=plt.cm.YlGnBu_r)


# ax2 = fig.add_axes([0.1, 0.85, 0.8, 0.1])

# s = Slider(ax = ax2, label = 'value', valmin = 0, valmax = 9, valinit = 3, valstep=1)

# def update(val):
#     # fig.canvas.flush_events()
#     value = s.val
#     ax.cla()
#     plt.title(f'n: {value}')
#     ax.plot_surface(X, Y, B[value], cmap = plt.cm.YlGnBu_r)
#     ax.set_zlim(np.amin(B[value]), np.amax(B[value]))
#     # ax.set_zlim(-2, 7)
#     # fig.canvas.draw()

# s.on_changed(update)
# update(0)

plt.show()