# MagneticFieldSolver
MagneticFieldSolver.py calculates the magnetic field created from a coil. By inputing the coil geometery, and the radius and z values you want the magnetic field to be calculated in. The script then writes the magneticField to a csv-file so that it can be plotted or further manipulated.

# Plot from csv
plotFromCsv.py takes in a csv-file of a magnetic field and makes a 3d-graph of the plot. With the slider you can change the Z value, to see how the field changes with respect to Z.

# Total field through loop
TotalFieldThroughLoop.py calculates the sum of the magnetic field a loop with a given radius will "see".

Features to be added:
* Offset between coil and loop in the xy-plane
* Calculate electromotive force (EMF) for a given current (I(t))
