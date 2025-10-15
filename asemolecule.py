#!/usr/bin/env python3
# Interactive 3D viewer via ASE (opens a window you can rotate/zoom)
# on terminal type: pip install ase
from ase.build import molecule
from ase.visualize import view

# Build water (H2O) with sensible geometry
mol = molecule('H2O')  # uses standard bond length/angle

# Show interactive window
view(mol)  # this window stays open until you close it
