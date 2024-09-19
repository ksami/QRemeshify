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
from .props import MyPropertyGroup, QRPropertyGroup


class QUADWILD_PT_UIPanel(bpy.types.Panel):
    bl_idname = "QUADWILD_PT_UIPanel"
    bl_label = "Quadwild Remesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Remesh"

    def draw(self, ctx: bpy.types.Context):
        props = ctx.scene.quadwild_props
        qr_props = ctx.scene.quadpatches_props
        layout = self.layout

        col = layout.column()
        col.prop(props, "debug")

        col.separator()

        col.prop(props, "enableRemesh")
        col.prop(props, "enableSharp")
        col.prop(props, "sharpAngle")

        row = col.row(align=True, heading="Symmetry")
        row.prop(props, "symmetryX", expand=True, toggle=1)
        row.prop(props, "symmetryY", expand=True, toggle=1)
        row.prop(props, "symmetryZ", expand=True, toggle=1)

        col.separator()

        col.prop(qr_props, "scaleFact")
        col.prop(qr_props, "fixedChartClusters")

        col.separator()

        # TODO: add presets based on config/prep_config and config/main_config/flow_*.txt
        col.prop(qr_props, "alpha")
        col.prop(qr_props, "ilpMethod")
        col.prop(qr_props, "timeLimit")
        col.prop(qr_props, "gapLimit")
        col.prop(qr_props, "minimumGap")
        col.prop(qr_props, "isometry")
        col.prop(qr_props, "regularityQuadrilaterals")
        col.prop(qr_props, "regularityNonQuadrilaterals")
        col.prop(qr_props, "regularityNonQuadrilateralsWeight")
        col.prop(qr_props, "alignSingularities")
        col.prop(qr_props, "alignSingularitiesWeight")
        col.prop(qr_props, "repeatLosingConstraintsIterations")
        col.prop(qr_props, "repeatLosingConstraintsQuads")
        col.prop(qr_props, "repeatLosingConstraintsNonQuads")
        col.prop(qr_props, "repeatLosingConstraintsAlign")
        col.prop(qr_props, "hardParityConstraint")

        col.prop(qr_props, "flowConfig")
        col.prop(qr_props, "satsumaConfig")


        # TODO: split into 3 operators for advanced mode to tweak indiv steps
        col.operator(QUADWILD_OT_REMESH.bl_idname)


def register():
    bpy.utils.register_class(QRPropertyGroup)
    bpy.utils.register_class(MyPropertyGroup)
    bpy.utils.register_class(QUADWILD_PT_UIPanel)
    bpy.utils.register_class(QUADWILD_OT_REMESH)

    bpy.types.Scene.quadwild_props = bpy.props.PointerProperty(type=MyPropertyGroup)
    bpy.types.Scene.quadpatches_props = bpy.props.PointerProperty(type=QRPropertyGroup)

def unregister():
    bpy.utils.unregister_class(QUADWILD_OT_REMESH)
    bpy.utils.unregister_class(QUADWILD_PT_UIPanel)

    bpy.utils.unregister_class(MyPropertyGroup)
    bpy.utils.unregister_class(QRPropertyGroup)
    del bpy.types.Scene.quadwild_props
    del bpy.types.Scene.quadpatches_props


if __name__ == "__main__":
    register()
