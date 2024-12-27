import numpy as np
import magpylib as magpy
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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







# Create a function to update the current and position, and return the updated figure
def update_figure(current1, current2, current3):
    for n, braunbek_part in enumerate(braunbek.children):
        for coil in braunbek_part:
            for winding in coil.children:
                if n == 0:
                    winding.current = current1
                if n == 1:
                    winding.current = current2
                if n == 2:
                    winding.current = current3

    # update the sensor
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
    
    fig = magpy.show(braunbek, sensor, backend='plotly', return_fig=True)
    return fig

# Create frames for different current and position values
currents1 = np.linspace(-1, 1, 5)
currents2 = np.linspace(-1, 1, 5)
currents3 = np.linspace(-1, 1, 5)

frames = []
for current1 in currents1:
    for current2 in currents2:
        for current3 in currents3:
            frame = go.Frame(
                data=update_figure(current1, current2, current3).data,
                name=f'current1_{current1:.2f}_current2_{current2:.2f}_current3_{current3:.2f}'
            )
            frames.append(frame)

# Create the initial figure
initial_fig = update_figure(-1, -1, -1)

# Create the final figure with frames and sliders
fig = go.Figure(
    data=initial_fig.data,
    layout=initial_fig.layout,
    frames=frames
)

# Add sliders
"""
sliders = [
    dict(
        active=10,
        currentvalue={"prefix": "Currents: "},
        pad={"t": 50},
        steps=[dict(
            method='animate',
            args=[[f'current1_{current1:.2f}_current2_{current2:.2f}_current3_{current3:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{current1:.2f} {current2:.2f} {current3:.2f}'
        ) for current1 in currents1 for current2 in currents2 for current3 in currents3]
    )
]
"""
sliders = [
    dict(
        active=0,
        currentvalue={"prefix": "Current 1: "},
        pad={"t": 50},
        steps=[dict(
            method='animate',
            args=[[f'current1_{current1:.2f}_current2_{-1:.2f}_current3_{-1:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{current1:.2f}'
        ) for current1 in currents1]
    ),
    dict(
        active=0,
        currentvalue={"prefix": "Current 2: "},
        pad={"t": 150},
        steps=[dict(
            method='animate',
            args=[[f'current1_{-1:.2f}_current2_{current2:.2f}_current3_{-1:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{current2:.2f}'
        ) for current2 in currents2]
    ),
    dict(
        active=0,
        currentvalue={"prefix": "Current 3: "},
        pad={"t": 250},
        steps=[dict(
            method='animate',
            args=[[f'current1_{-1:.2f}_current2_{-1:.2f}_current3_{current3:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{current3:.2f}'
        ) for current3 in currents3]
    )
]

fig.update_layout(
    sliders=sliders,
    title='Braunbek Coil Visualization',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='data'
    )
)

fig.show()
