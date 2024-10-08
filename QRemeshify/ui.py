from bpy.types import Context, Panel
from .operator import QREMESH_OT_Remesh


class BasePanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QRemeshify"
    bl_context = 'objectmode'


class QREMESH_PT_UIPanel(BasePanel, Panel):
    bl_idname = "QREMESH_PT_UIPanel"
    bl_label = "QRemeshify"

    def draw(self, ctx: Context):
        props = ctx.scene.quadwild_props
        qr_props = ctx.scene.quadpatches_props

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        row = layout.row()
        col = layout.column(heading="Enable")
        col.prop(props, "enableRemesh")
        col.prop(props, "enableSmoothing")

        layout.separator(factor=0.1)

        row = layout.row()
        col = row.column(heading="Sharp Detect")
        row = col.row()
        row.prop(props, "enableSharp", text="")
        row.prop(props, "sharpAngle", text="Angle")

        layout.separator(factor=0.1)

        row = layout.row(align=True, heading="Symmetry")
        row.prop(props, "symmetryX", expand=True, toggle=1)
        row.prop(props, "symmetryY", expand=True, toggle=1)
        row.prop(props, "symmetryZ", expand=True, toggle=1)

        layout.separator(factor=0.1)

        row = layout.row()
        row.prop(qr_props, "scaleFact", text="Density")

        layout.separator()

        layout.label(icon="ERROR", text="Please save first, remesh may be slow")
        layout.operator(QREMESH_OT_Remesh.bl_idname, icon="MESH_GRID")


class QREMESH_PT_UIAdvancedPanel(BasePanel, Panel):
    bl_parent_id = "QREMESH_PT_UIPanel"
    bl_label = "Advanced"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, ctx: Context):
        props = ctx.scene.quadwild_props
        qr_props = ctx.scene.quadpatches_props

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        row = layout.row()
        col = row.column()
        col.prop(props, "debug")
        col.prop(props, "useCache")

        layout.separator(type="LINE")

        row = layout.row()
        col = row.column()
        col.prop(qr_props, "flowConfig")
        col.prop(qr_props, "satsumaConfig")

        layout.separator(factor=0.1)

        row = layout.row()
        col = row.column()
        col.prop(qr_props, "alpha")
        col.prop(qr_props, "ilpMethod")

        layout.separator(type="LINE")

        row = layout.row()
        col = row.column(heading="Regularity")
        col.prop(qr_props, "regularityQuadrilaterals", text="Quadrilaterals")
        col.prop(qr_props, "regularityNonQuadrilaterals", text="Non Quadrilaterals")
        col.prop(qr_props, "regularityNonQuadrilateralsWeight")

        layout.separator(factor=0.1)

        row = layout.row()
        col = row.column(heading="Align")
        col.prop(qr_props, "alignSingularities", text="Singularities")
        col.prop(qr_props, "alignSingularitiesWeight")

        layout.separator(factor=0.1)

        row = layout.row()
        col = row.column(heading="Repeat Losing Constraints")
        col.prop(qr_props, "repeatLosingConstraintsIterations", text="Iterations")
        col.prop(qr_props, "repeatLosingConstraintsQuads", text="Quads")
        col.prop(qr_props, "repeatLosingConstraintsNonQuads", text="NonQuads")
        col.prop(qr_props, "repeatLosingConstraintsAlign", text="Align")

        layout.separator(type="LINE")

        row = layout.row()
        col = row.column()
        col.prop(qr_props, "fixedChartClusters")
        col.prop(qr_props, "timeLimit")
        col.prop(qr_props, "gapLimit")
        col.prop(qr_props, "minimumGap")
        col.prop(qr_props, "isometry")
        col.prop(qr_props, "hardParityConstraint")

class QREMESH_PT_UICallbackPanel(BasePanel, Panel):
    bl_parent_id = "QREMESH_PT_UIAdvancedPanel"
    bl_label = "Callback Limits"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, ctx: Context):
        qr_props = ctx.scene.quadpatches_props

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        col = layout.column()
        col.prop(qr_props, "callbackTimeLimit", text="Time Limit")
        col.prop(qr_props, "callbackGapLimit", text="Gap Limit")
