import magpylib as magpy
import numpy as np

# Define magnet with path
magnet = magpy.magnet.Cylinder(
    polarization=(1, 0, 0),
    dimension=(2, 1),
    position=(4, 0, 0),
    style_label="magnet",
)
magnet.rotate_from_angax(angle=np.linspace(0, 300, 40), start=0, axis="z", anchor=0)

# Define sensor with path
sensor = magpy.Sensor(
    pixel=[(-0.2, 0, 0), (0.2, 0, 0)],
    position=np.linspace((0, 0, -3), (0, 0, 3), 40),
    style_label="sensor",
)

# Display as animation - prefers plotly backend
magpy.show(sensor, magnet, animation=True, backend="plotly")