import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt
from math import sqrt

# Set some parameters for the design
WIRE_DIAMETER = 1 # [mm]
INNER_COIL_DIAMETER = 100 # [mm]
WINDINGS_PER_COIL = 4
CURRENT = 1 # [A]

# Create a finite sized Helmholtz coil-pair
coil1 = magpy.Collection()
windingcount = 0
for n1 in range(int(sqrt(WINDINGS_PER_COIL))):
    for n2 in range(int(sqrt(WINDINGS_PER_COIL))):
        windingcount = windingcount + 1
        winding = magpy.current.Circle(
            current=CURRENT,
            diameter=INNER_COIL_DIAMETER/1000 + n2 * WIRE_DIAMETER/1000,
            position=(0, 0, (n1+0.5)*WIRE_DIAMETER/1000), # offset by 1/2 diameter
        )
        coil1.add(winding)
print(f"Using {windingcount} windings per coil")

coil1.position = (0,0,INNER_COIL_DIAMETER/4000)
coil2 = coil1.copy(position=(0,0,-INNER_COIL_DIAMETER/4000))
helmholtz1 = magpy.Collection(coil1, coil2)



# Create a finite sized Helmholtz coil-pair
coil3 = magpy.Collection()
windingcount = 0
for n1 in range(int(sqrt(WINDINGS_PER_COIL))):
    for n2 in range(int(sqrt(WINDINGS_PER_COIL))):
        windingcount = windingcount + 1
        winding = magpy.current.Circle(
            current=CURRENT,
            diameter=INNER_COIL_DIAMETER/1000 + n2 * WIRE_DIAMETER/1000,
            position=(0, 0, (n1+0.5)*WIRE_DIAMETER/1000), # offset by 1/2 diameter
        )
        coil3.add(winding)
print(f"Using {windingcount} windings per coil")

coil3.position = (0, 0, INNER_COIL_DIAMETER/4000)
coil3.rotate_from_angax(-90, "x", anchor=0, start=0)
coil4 = coil3.copy(position=(0, -INNER_COIL_DIAMETER/4000, 0))
helmholtz2 = magpy.Collection(coil3, coil4)
helmholtz2.show()



helmholtz_2d = magpy.Collection(helmholtz1, helmholtz2)
helmholtz_2d.show()

print(f"Field in center: {magpy.getB(helmholtz_2d, [0, 0, 0])}")



fig, axes = plt.subplots(1, 2, figsize=(6,5))

ax = axes[0]

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -0.5:0.5:20j, -0.5:0.5:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = magpy.getB(helmholtz_2d, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax.streamplot(Y, Z, By, Bz, density=2, color=Bamp,
    linewidth=np.sqrt(Bamp)*3, cmap='coolwarm',
)

# Plot coil outline
#from matplotlib.patches import Rectangle
#for loc in [(4,4), (4,-6), (-6,4), (-6,-6)]:
#    ax.add_patch(Rectangle(loc, 2, 2, color='k', zorder=10))

# Figure styling
ax.set(
    title='Magnetic field of Helmholtz',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=ax, label='(T)')



ax2 = axes[1]

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -0.1:0.1:20j, -0.1:0.1:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = magpy.getB(helmholtz_2d, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax2.streamplot(Y, Z, By, Bz, density=2, color=Bamp,
    linewidth=np.sqrt(Bamp)*3, cmap='coolwarm',
)

# Plot coil outline
#from matplotlib.patches import Rectangle
#for loc in [(4,4), (4,-6), (-6,4), (-6,-6)]:
#    ax.add_patch(Rectangle(loc, 2, 2, color='k', zorder=10))

# Figure styling
ax2.set(
    title='Magnetic field of Helmholtz',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=ax2, label='(T)')



plt.tight_layout()
plt.show()