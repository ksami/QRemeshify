bl_info = {
    "name": "QRemeshify",
    "description": "Remesher with good-quality quad topology",
    "author": "ksami",
    "version": (1, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D",
    "category": "Mesh",
}


import bpy
from .operator import QREMESH_OT_Remesh
from .props import QWPropertyGroup, QRPropertyGroup
from .ui import QREMESH_PT_UIPanel, QREMESH_PT_UIAdvancedPanel, QREMESH_PT_UICallbackPanel


classes = [
    QWPropertyGroup,
    QRPropertyGroup,
    QREMESH_PT_UIPanel,
    QREMESH_PT_UIAdvancedPanel,
    QREMESH_PT_UICallbackPanel,
    QREMESH_OT_Remesh,
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
