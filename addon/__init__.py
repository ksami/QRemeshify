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
from .props import MyPropertyGroup


class QUADWILD_PT_UIPanel(bpy.types.Panel):
    bl_idname = "QUADWILD_PT_UIPanel"
    bl_label = "Quadwild Remesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Remesh"

    def draw(self, ctx: bpy.types.Context):
        props = ctx.scene.quadwild_props
        layout = self.layout

        col = layout.column()
        col.prop(props, "remesh")
        col.prop(props, "sharpAngle")  # TODO: replace using edges marked sharp/seam

        # Doesn't seem to have effect
        # col.prop(props, "alpha")
        # col.prop(props, "scaleFact")

        col.operator(QUADWILD_OT_REMESH.bl_idname)

        progress_factor = props.progress_factor
        if progress_factor < 0.01:
            progress_text = ""
        else:
            if progress_factor > 0.999:
                progress_text = "Done"
            else:
                progress_text = "Running..."
            col.progress(type='BAR', factor=progress_factor, text=progress_text)



def register():
    bpy.utils.register_class(MyPropertyGroup)
    bpy.utils.register_class(QUADWILD_PT_UIPanel)
    bpy.utils.register_class(QUADWILD_OT_REMESH)

    bpy.types.Scene.quadwild_props = bpy.props.PointerProperty(type=MyPropertyGroup)

def unregister():
    bpy.utils.unregister_class(QUADWILD_OT_REMESH)
    bpy.utils.unregister_class(QUADWILD_PT_UIPanel)

    bpy.utils.unregister_class(MyPropertyGroup)
    del bpy.types.Scene.quadwild_props


if __name__ == "__main__":
    register()
