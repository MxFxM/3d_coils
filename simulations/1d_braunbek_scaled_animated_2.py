import numpy as np
import magpylib as magpy
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# From: https://gfzpublic.gfz-potsdam.de/rest/items/item_3142899_2/component/file_3169935/content

ORIG_R1 = 0.780 # diameter of inner coils
ORIG_R2 = 0.596 # diameter of outer coils
ORIG_D1 = 0.108 # distance of inner coils
ORIG_D2 = 0.330 # distance of outer coils

SCALING = 0.030/ORIG_D1

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

# Create a function to update the current and position, and return the updated figure
def update_figure(current, position_factor):
    for coil in braunbek.children:
        for winding in coil.children:
            winding.current = current
    
    # Update position of outer coils
    braunbek.children[0].children[0].position = (0, 0, D2 * position_factor)
    braunbek.children[3].children[0].position = (0, 0, -D2 * position_factor)
    
    fig = magpy.show(braunbek, backend='plotly', return_fig=True)
    return fig

# Create frames for different current and position values
currents = np.linspace(0.1, 2, 20)
positions = np.linspace(0.5, 1.5, 20)

frames = []
for current in currents:
    for position in positions:
        frame = go.Frame(
            data=update_figure(current, position).data,
            name=f'current_{current:.2f}_position_{position:.2f}'
        )
        frames.append(frame)

# Create the initial figure
initial_fig = update_figure(1, 1)

# Create the final figure with frames and sliders
fig = go.Figure(
    data=initial_fig.data,
    layout=initial_fig.layout,
    frames=frames
)

# Add sliders
sliders = [
    dict(
        active=10,
        currentvalue={"prefix": "Current: "},
        pad={"t": 50},
        steps=[dict(
            method='animate',
            args=[[f'current_{current:.2f}_position_{1:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{current:.2f}'
        ) for current in currents]
    ),
    dict(
        active=10,
        currentvalue={"prefix": "Position factor: "},
        pad={"t": 100},
        steps=[dict(
            method='animate',
            args=[[f'current_{1:.2f}_position_{position:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=f'{position:.2f}'
        ) for position in positions]
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
