import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt

# Create a finite sized Helmholtz coil-pair
coil1 = magpy.Collection()
for z in np.linspace(-1, 1, 5):
    for r in np.linspace(4, 5, 5):
        winding = magpy.current.Circle(
            current=10,
            diameter=2*r,
            position=(0,0,z),
        )
        coil1.add(winding)

coil1.position = (0,0,5)
coil2 = coil1.copy(position=(0,0,-5))

helmholtz = magpy.Collection(coil1, coil2)

helmholtz.show()

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