import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt
from math import sqrt

# From: https://gfzpublic.gfz-potsdam.de/rest/items/item_3142899_2/component/file_3169935/content

ORIG_R1 = 0.780 # diameter of inner coils
ORIG_R2 = 0.596 # diameter of outer coils
ORIG_D1 = 0.108 # distance of inner coils
ORIG_D2 = 0.330 # distance of outer coils

SCALING = 0.035/ORIG_D1

R1 = ORIG_R1 * SCALING
R2 = ORIG_R2 * SCALING
D1 = ORIG_D1 * SCALING
D2 = ORIG_D2 * SCALING

print()
print("Design:")
print(f"Outer coils: d={R2*1000:.1f}mm positioned at +/-{D2*1000:.1f}mm")
print(f"Inner coils: d={R1*1000:.1f}mm positioned at +/-{D1*1000:.1f}mm")
print()

# Set some parameters for the design
CURRENT = 1 # [A]

# Create a finite sized Helmholtz coil-pair
coil1 = magpy.Collection()
winding1 = magpy.current.Circle(
    current=CURRENT,
    diameter=R2,
    position=(0, 0, D2),
)
coil1.add(winding1)

coil2 = magpy.Collection()
winding2 = magpy.current.Circle(
    current=CURRENT,
    diameter=R1,
    position=(0, 0, D1),
)
coil2.add(winding2)

coil3 = magpy.Collection()
winding3 = magpy.current.Circle(
    current=CURRENT,
    diameter=R1,
    position=(0, 0, -D1),
)
coil3.add(winding3)

coil4 = magpy.Collection()
winding4 = magpy.current.Circle(
    current=CURRENT,
    diameter=R2,
    position=(0, 0, -D2),
)
coil4.add(winding4)

braunbek = magpy.Collection(coil1, coil2, coil3, coil4)

magpy.show({"objects":braunbek},
           backend="plotly")

print(f"Field in center: {magpy.getB(braunbek, [0, 0, 0])}")



fig, ax = plt.subplots(1, 1, figsize=(6,5))

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -0.05:0.05:20j, -0.05:0.05:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = magpy.getB(braunbek, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax.streamplot(Y, Z, By, Bz, density=5, color=Bamp,
    linewidth=np.sqrt(Bamp)*3, cmap='coolwarm',
)

# Plot coil outline
#from matplotlib.patches import Rectangle
#for loc in [(4,4), (4,-6), (-6,4), (-6,-6)]:
#    ax.add_patch(Rectangle(loc, 2, 2, color='k', zorder=10))

# Figure styling
ax.set(
    title='Magnetic field of Braunbek',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=ax, label='(T)')



plt.tight_layout()
plt.show()