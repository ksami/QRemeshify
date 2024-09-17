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
from .operator import QUADWILD_OT_REMESH


class QUADWILD_PT_UIPanel(bpy.types.Panel):
    bl_idname = "QUADWILD_PT_UIPanel"
    bl_label = "Quadwild Remesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Remesh"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator(QUADWILD_OT_REMESH.bl_idname)
        col.progress(factor= 0.7, type = 'BAR', text = "Updating")
        col.progress(factor= 0.7, type = 'RING', text = "Updating...")


def register():
    bpy.utils.register_class(QUADWILD_PT_UIPanel)
    bpy.utils.register_class(QUADWILD_OT_REMESH)

def unregister():
    bpy.utils.unregister_class(QUADWILD_OT_REMESH)
    bpy.utils.unregister_class(QUADWILD_PT_UIPanel)


if __name__ == "__main__":
    register()
