import bpy
import os
from .lib import Quadwild, Parameters


class QUADWILD_OT_REMESH(bpy.types.Operator):
    """Remesh with Quadwild"""
    bl_idname = "quadwild.remesh"
    bl_label = "Remesh"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, ctx):
        props = ctx.scene.quadwild_props

        obj = ctx.active_object
        if obj.type != 'MESH':
            self.report({'INFO'}, "Selection isn't a mesh object")
            return {'CANCELLED'}

        if len(obj.data.polygons) == 0:
            self.report({'ERROR'}, "Mesh has 0 faces")
            return {'CANCELLED'}

        props.progress_factor = 0.0

        obj = ctx.active_object
        mesh_name = os.path.join(bpy.app.tempdir, obj.name)
        mesh_filepath = f"{mesh_name}.obj"
        self.report({'INFO'}, f"Remeshing from {mesh_filepath}")

        # Export selected object as OBJ
        bpy.ops.wm.obj_export(filepath=mesh_filepath, check_existing=False, export_selected_objects=True, export_materials=False)
        props.progress_factor = 0.1

        # Load lib
        qw = Quadwild(mesh_filepath)
        props.progress_factor = 0.2

        # Remesh and calculate field
        qw.remeshAndField(params=Parameters(
            remesh=props.remesh,
            sharpAngle=props.sharpAngle,
            alpha=props.alpha,
            scaleFact=props.scaleFact,
            hasFeature=False,
            hasField=False,
        ))
        props.progress_factor = 0.5

        # Trace
        qw.trace()
        props.progress_factor = 0.8

        # Convert to quads
        qw.quadrangulate()
        qw = None
        props.progress_factor = 1.0

        # Import remeshed OBJ
        mesh_filepath = f"{mesh_name}_rem_p0_0_quadrangulation_smooth.obj"
        bpy.ops.wm.obj_import(filepath=mesh_filepath, check_existing=True)
        newest_obj = ctx.scene.objects[-1]
        newest_obj.name = f"{obj.name} Remeshed"

        # Hide original
        obj.hide_set(True)

        return {'FINISHED'}
