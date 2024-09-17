from bpy.types import PropertyGroup
from bpy.props import *


class MyPropertyGroup(PropertyGroup):
    progress_factor:    FloatProperty(name="Progress %", description="Progress of operator", min=0, max=1, default=0, subtype="FACTOR")
