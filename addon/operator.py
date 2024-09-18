import bpy
import os
from .lib import Quadwild, Parameters
from .util.export import export_sharp_features


class QUADWILD_OT_REMESH(bpy.types.Operator):
    """Remesh with Quadwild"""
    bl_idname = "quadwild.remesh"
    bl_label = "Remesh"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, ctx):
        props = ctx.scene.quadwild_props

        obj = ctx.object
        if obj.type != 'MESH':
            self.report({'INFO'}, "Object isn't a mesh object")
            return {'CANCELLED'}

        if len(obj.data.polygons) == 0:
            self.report({'ERROR'}, "Mesh has 0 faces")
            return {'CANCELLED'}

        # Get mesh after modifiers and shapekeys applied
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_obj = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated_obj, depsgraph=depsgraph)

        # TODO: discard half if symmetrize

        props.progress_factor = 0.0

        mesh_name = os.path.join(bpy.app.tempdir, obj.name)
        mesh_filepath = f"{mesh_name}.obj"
        self.report({'INFO'}, f"Remeshing from {mesh_filepath}")

        # Export selected object as OBJ
        bpy.ops.wm.obj_export(filepath=mesh_filepath, apply_modifiers=True, check_existing=False, export_selected_objects=True, export_materials=False)
        props.progress_factor = 0.1

        # Load lib
        qw = Quadwild(mesh_filepath)
        props.progress_factor = 0.2

        # Calculate sharp
        export_sharp_features(mesh, qw.sharp_path, props.sharpAngle)
        props.progress_factor = 0.25

        # Remesh and calculate field
        qw.remeshAndField(params=Parameters(
            remesh=props.remesh,
            sharpAngle=props.sharpAngle,
            alpha=props.alpha,
            scaleFact=props.scaleFact,
            hasFeature=True,
            hasField=False,
        ))
        props.progress_factor = 0.6

        # Trace
        qw.trace()
        props.progress_factor = 0.8

        # Convert to quads
        qw.quadrangulate()
        props.progress_factor = 0.95

        # Import remeshed OBJ
        bpy.ops.wm.obj_import(filepath=qw.output_smoothed_path,  check_existing=True)
        imported_obj = ctx.selected_objects[0]
        imported_obj.name = f"{obj.name} Remeshed"

        # Hide original
        obj.hide_set(True)
        del qw
        props.progress_factor = 1.0

        return {'FINISHED'}
