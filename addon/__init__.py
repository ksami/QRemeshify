bl_info = {
    "name": "Test Addon",
    "description": "Addon for testing",
    "author": "Tester",
    "blender": (4, 2, 0),
    "version": (0, 0, 1),
    "category": "Test",
    "location": "View3D > UI > Test addon operator",
}


import bpy
from .operator import QUADWILD_OT_Remesh
from .props import QWPropertyGroup, QRPropertyGroup
from .ui import QUADWILD_PT_UIPanel, QUADWILD_PT_UIAdvancedPanel, QUADWILD_PT_UICallbackPanel


classes = [
    QWPropertyGroup,
    QRPropertyGroup,
    QUADWILD_PT_UIPanel,
    QUADWILD_PT_UIAdvancedPanel,
    QUADWILD_PT_UICallbackPanel,
    QUADWILD_OT_Remesh,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.quadwild_props = bpy.props.PointerProperty(type=QWPropertyGroup)
    bpy.types.Scene.quadpatches_props = bpy.props.PointerProperty(type=QRPropertyGroup)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.quadwild_props
    del bpy.types.Scene.quadpatches_props


if __name__ == "__main__":
    register()
