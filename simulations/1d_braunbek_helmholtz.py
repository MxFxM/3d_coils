import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt
from math import sqrt

# From: https://gfzpublic.gfz-potsdam.de/rest/items/item_3142899_2/component/file_3169935/content

# Set some parameters for the design
CURRENT = 1 # [A]

# Create a finite sized Helmholtz coil-pair
coil1 = magpy.Collection()
winding1 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.596,
    position=(0, 0, 0.330),
)
coil1.add(winding1)

coil2 = magpy.Collection()
winding2 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.780,
    position=(0, 0, 0.108),
)
coil2.add(winding2)

coil3 = magpy.Collection()
winding3 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.780,
    position=(0, 0, -0.108),
)
coil3.add(winding3)

coil4 = magpy.Collection()
winding4 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.596,
    position=(0, 0, -0.330),
)
coil4.add(winding4)

braunbek = magpy.Collection(coil1, coil2, coil3, coil4)
print(f"Field in braunbek: {magpy.getB(braunbek, [0, 0, 0])}")
braunbek.show()

coil5 = magpy.Collection()
winding5 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.432,
    position=(0, 0, 0.108),
)
coil5.add(winding5)

coil6 = magpy.Collection()
winding6 = magpy.current.Circle(
    current=CURRENT,
    diameter=0.432,
    position=(0, 0, -0.108),
)
coil6.add(winding6)

helmholtz = magpy.Collection(coil5, coil6)
print(f"Field in helmholtz: {magpy.getB(helmholtz, [0, 0, 0])}")
helmholtz.show()



fig, axes = plt.subplots(1, 2, figsize=(6,5))

braunbek_ax = axes[0]
helmholtz_ax = axes[1]

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -0.5:0.5:20j, -0.5:0.5:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

braunbek_B = magpy.getB(braunbek, grid)
_, braunbek_By, braunbek_Bz = np.moveaxis(braunbek_B, 2, 0)

braunbek_Bamp = np.linalg.norm(braunbek_B, axis=2)
braunbek_Bamp /= np.amax(braunbek_Bamp)

sp = braunbek_ax.streamplot(Y, Z, braunbek_By, braunbek_Bz, density=2, color=braunbek_Bamp,
    linewidth=np.sqrt(braunbek_Bamp)*3, cmap='coolwarm',
)

# Figure styling
braunbek_ax.set(
    title='Magnetic field of Braunbek',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=braunbek_ax, label='(T)')

helmholtz_B = magpy.getB(helmholtz, grid)
_, helmholtz_By, helmholtz_Bz = np.moveaxis(helmholtz_B, 2, 0)

helmholtz_Bamp = np.linalg.norm(helmholtz_B, axis=2)
helmholtz_Bamp /= np.amax(helmholtz_Bamp)

sp = helmholtz_ax.streamplot(Y, Z, helmholtz_By, helmholtz_Bz, density=2, color=helmholtz_Bamp,
    linewidth=np.sqrt(helmholtz_Bamp)*3, cmap='coolwarm',
)

# Figure styling
helmholtz_ax.set(
    title='Magnetic field of Braunbek',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=helmholtz_ax, label='(T)')

plt.tight_layout()
plt.show()



fig, axes = plt.subplots(1, 2, figsize=(6,5))

braunbek_ax = axes[0]
helmholtz_ax = axes[1]

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -0.2:0.2:20j, -0.2:0.2:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

braunbek_B = magpy.getB(braunbek, grid)
_, braunbek_By, braunbek_Bz = np.moveaxis(braunbek_B, 2, 0)

braunbek_Bamp = np.linalg.norm(braunbek_B, axis=2)
braunbek_Bamp /= np.amax(braunbek_Bamp)

sp = braunbek_ax.streamplot(Y, Z, braunbek_By, braunbek_Bz, density=2, color=braunbek_Bamp,
    linewidth=np.sqrt(braunbek_Bamp)*3, cmap='coolwarm',
)

# Figure styling
braunbek_ax.set(
    title='Magnetic field of Braunbek',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)

helmholtz_B = magpy.getB(helmholtz, grid)
_, helmholtz_By, helmholtz_Bz = np.moveaxis(helmholtz_B, 2, 0)

helmholtz_Bamp = np.linalg.norm(helmholtz_B, axis=2)
helmholtz_Bamp /= np.amax(helmholtz_Bamp)

sp = helmholtz_ax.streamplot(Y, Z, helmholtz_By, helmholtz_Bz, density=5, color=helmholtz_Bamp,
    linewidth=np.sqrt(helmholtz_Bamp)*3, cmap='coolwarm',
)

# Figure styling
helmholtz_ax.set(
    title='Magnetic field of Braunbek',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)

plt.tight_layout()
plt.show()