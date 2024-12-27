import numpy as np
import magpylib as magpy

# From: https://gfzpublic.gfz-potsdam.de/rest/items/item_3142899_2/component/file_3169935/content

ORIG_R1 = 0.780 # diameter of inner coils
ORIG_R2 = 0.596 # diameter of outer coils
ORIG_D1 = 0.108 # distance of inner coils
ORIG_D2 = 0.330 # distance of outer coils

SCALING1 = 0.030/ORIG_D1
SCALING2 = 0.035/ORIG_D1
SCALING3 = 0.040/ORIG_D1

color1 = "blue"
color2 = "darkgreen"
color3 = "red"

# Set some parameters for the design
CURRENT1 = 0 # [A]
CURRENT2 = 1 # [A]
CURRENT3 = 1 # [A]

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

# Create a finite sized Helmholtz coil-pair
#######################################################################################################################
R1 = ORIG_R1 * SCALING1
R2 = ORIG_R2 * SCALING1
D1 = ORIG_D1 * SCALING1
D2 = ORIG_D2 * SCALING1
print()
print("1st Axis")
print(f"Outer coils: d={R2*1000:.1f}mm positioned at +/-{D2*1000:.1f}mm")
print(f"Inner coils: d={R1*1000:.1f}mm positioned at +/-{D1*1000:.1f}mm")

coil1 = magpy.Collection()
winding1 = magpy.current.Circle(
    current=CURRENT1,
    diameter=R2,
    position=(0, 0, D2),
)
coil1.add(winding1)

coil2 = magpy.Collection()
winding2 = magpy.current.Circle(
    current=CURRENT1,
    diameter=R1,
    position=(0, 0, D1),
)
coil2.add(winding2)

coil3 = magpy.Collection()
winding3 = magpy.current.Circle(
    current=CURRENT1,
    diameter=R1,
    position=(0, 0, -D1),
)
coil3.add(winding3)

coil4 = magpy.Collection()
winding4 = magpy.current.Circle(
    current=CURRENT1,
    diameter=R2,
    position=(0, 0, -D2),
)
coil4.add(winding4)

braunbek1 = magpy.Collection(coil1, coil2, coil3, coil4)
braunbek1.set_children_styles(color=color1)

#######################################################################################################################
R1 = ORIG_R1 * SCALING2
R2 = ORIG_R2 * SCALING2
D1 = ORIG_D1 * SCALING2
D2 = ORIG_D2 * SCALING2
print()
print("2nd Axis")
print(f"Outer coils: d={R2*1000:.1f}mm positioned at +/-{D2*1000:.1f}mm")
print(f"Inner coils: d={R1*1000:.1f}mm positioned at +/-{D1*1000:.1f}mm")

coil5 = magpy.Collection()
winding5 = magpy.current.Circle(
    current=CURRENT2,
    diameter=R2,
    position=(0, 0, D2),
)
coil5.add(winding5)

coil6 = magpy.Collection()
winding6 = magpy.current.Circle(
    current=CURRENT2,
    diameter=R1,
    position=(0, 0, D1),
)
coil6.add(winding6)

coil7 = magpy.Collection()
winding7 = magpy.current.Circle(
    current=CURRENT2,
    diameter=R1,
    position=(0, 0, -D1),
)
coil7.add(winding7)

coil8 = magpy.Collection()
winding8 = magpy.current.Circle(
    current=CURRENT2,
    diameter=R2,
    position=(0, 0, -D2),
)
coil8.add(winding8)

braunbek2 = magpy.Collection(coil5, coil6, coil7, coil8)
braunbek2.set_children_styles(color=color2)
braunbek2.rotate_from_angax(-90, "x", anchor=0, start=0)

#######################################################################################################################
R1 = ORIG_R1 * SCALING3
R2 = ORIG_R2 * SCALING3
D1 = ORIG_D1 * SCALING3
D2 = ORIG_D2 * SCALING3
print()
print("3rd Axis")
print(f"Outer coils: d={R2*1000:.1f}mm positioned at +/-{D2*1000:.1f}mm")
print(f"Inner coils: d={R1*1000:.1f}mm positioned at +/-{D1*1000:.1f}mm")
print()

coil9 = magpy.Collection()
winding9 = magpy.current.Circle(
    current=CURRENT3,
    diameter=R2,
    position=(0, 0, D2),
)
coil9.add(winding9)

coil10 = magpy.Collection()
winding10 = magpy.current.Circle(
    current=CURRENT3,
    diameter=R1,
    position=(0, 0, D1),
)
coil10.add(winding10)

coil11 = magpy.Collection()
winding11 = magpy.current.Circle(
    current=CURRENT3,
    diameter=R1,
    position=(0, 0, -D1),
)
coil11.add(winding11)

coil12 = magpy.Collection()
winding12 = magpy.current.Circle(
    current=CURRENT3,
    diameter=R2,
    position=(0, 0, -D2),
)
coil12.add(winding12)

braunbek3 = magpy.Collection(coil9, coil10, coil11, coil12)
braunbek3.set_children_styles(color=color3)
braunbek3.rotate_from_angax(90, "y", anchor=0, start=0)

braunbek = magpy.Collection(braunbek1, braunbek2, braunbek3)

sensor = magpy.Sensor(position=(0,0,0))
B = braunbek.getB(sensor.position)
vector_trace = {
    "backend": "plotly",
    "constructor": "Cone",
    "kwargs": {
        "x": [sensor.position[0]],
        "y": [sensor.position[1]],
        "z": [sensor.position[2]],
        "u": [B[0]],
        "v": [B[1]],
        "w": [B[2]],
        "colorscale": "Blues",
        "sizemode": "absolute",
        "sizeref": 0.1,
        "showscale": False,
    }
}
sensor.style.model3d.add_trace(vector_trace)

magpy.show({"objects":[braunbek1], "row":1, "col":1},
           {"objects":[braunbek2], "row":1, "col":2},
           {"objects":[braunbek3], "row":1, "col":3},
           {"objects":[braunbek, sensor], "row":2, "col":2},
           backend="plotly")

print(f"Field in center: {magpy.getB(braunbek, [0, 0, 0])}")



"""
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
"""