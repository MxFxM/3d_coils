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

# Create a function to update the current and return the updated figure
def update_figure(current):
    for coil in braunbek.children:
        for winding in coil.children:
            winding.current = current
    
    fig = magpy.show(braunbek, backend='plotly', return_fig=True)
    return fig

# Create frames for different current values
currents = np.linspace(0.1, 2, 20)
frames = [go.Frame(data=update_figure(current).data, name=f'current_{current:.2f}') for current in currents]

# Create the initial figure
initial_fig = update_figure(1)

# Create the final figure with frames and slider
fig = go.Figure(
    data=initial_fig.data,
    layout=initial_fig.layout,
    frames=frames
)

# Add slider
sliders = [dict(
    active=10,
    currentvalue={"prefix": "Current 1: "},
    pad={"t": 50},
    steps=[dict(
        method='animate',
        args=[[f'current_{current:.2f}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
        label=f'{current:.2f}'
    ) for current in currents]
)]

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
