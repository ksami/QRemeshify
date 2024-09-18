from bpy.types import PropertyGroup
from bpy.props import *


class MyPropertyGroup(PropertyGroup):
    progress_factor:    FloatProperty(name="Progress %", description="Progress of operator", min=0, max=1, default=0, subtype="FACTOR")

    remesh:             BoolProperty(name="Preprocess", description="Run preprocess to try to fix mesh", default=False)
    sharpAngle:         FloatProperty(name="Sharp Angle", description="Angle threshold for sharp edges", min=0, max=180, default=35, precision=2, step=1, subtype="FACTOR")
    alpha:              FloatProperty(name="Alpha", description="Smaller for more regularity", min=0, max=1, default=0.01, subtype="FACTOR")
    scaleFact:          FloatProperty(name="Scale", description="Smaller for smaller quads", min=0.01, max=2, default=1, subtype="FACTOR")
