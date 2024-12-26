import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt

# Set some parameters for the design
WIRE_DIAMETER = 1 # [mm]
INNER_COIL_DIAMETER = 100 # [mm]
WINDINGS_PER_COIL = 4
CURRENT = 1 # [A]

# Create a finite sized Helmholtz coil-pair
coil1 = magpy.Collection()
windingcount = 0
for n1 in range(WINDINGS_PER_COIL//2):
    for n2 in range(WINDINGS_PER_COIL//2):
        windingcount = windingcount + 1
        winding = magpy.current.Circle(
            current=CURRENT,
            diameter=INNER_COIL_DIAMETER + n2 * WIRE_DIAMETER,
            position=(0, 0, (n1+0.5)*WIRE_DIAMETER), # offset by 1/2 diameter
        )
        coil1.add(winding)
print(f"Using {windingcount} windings per coil")

coil1.position = (0,0,INNER_COIL_DIAMETER/4)
coil2 = coil1.copy(position=(0,0,-INNER_COIL_DIAMETER/4))
helmholtz = magpy.Collection(coil1, coil2)

helmholtz.show()

quit()

fig, ax = plt.subplots(1, 1, figsize=(6,5))

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -13:13:20j, -13:13:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = magpy.getB(helmholtz, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax.streamplot(Y, Z, By, Bz, density=2, color=Bamp,
    linewidth=np.sqrt(Bamp)*3, cmap='coolwarm',
)

# Plot coil outline
from matplotlib.patches import Rectangle
for loc in [(4,4), (4,-6), (-6,4), (-6,-6)]:
    ax.add_patch(Rectangle(loc, 2, 2, color='k', zorder=10))

# Figure styling
ax.set(
    title='Magnetic field of Helmholtz',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=ax, label='(T)')

plt.tight_layout()
plt.show()