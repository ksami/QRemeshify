import bmesh
import bpy
import os
from .lib import Quadwild, Parameters
from .util import export, bisect


class QUADWILD_OT_REMESH(bpy.types.Operator):
    """Remesh with Quadwild"""
    bl_idname = "quadwild.remesh"
    bl_label = "Remesh"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, ctx):
        props = ctx.scene.quadwild_props
        qr_props = ctx.scene.quadpatches_props
        selected_objs = ctx.selected_objects

        if len(selected_objs) == 0:
            self.report({'ERROR_INVALID_INPUT'}, "No selected objects")
            return {'CANCELLED'}

        if len(selected_objs) > 1:
            self.report({'INFO'}, "Multiple objects selected, will only operate on the first selected object")

        obj = selected_objs[0]
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR_INVALID_INPUT'}, "Object is not a mesh")
            return {'CANCELLED'}

        if len(obj.data.polygons) == 0:
            self.report({'ERROR_INVALID_INPUT'}, "Mesh has 0 faces")
            return {'CANCELLED'}


        # Get mesh after modifiers and shapekeys applied
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_obj = obj.evaluated_get(depsgraph)
        mesh = evaluated_obj.to_mesh()
        # mesh = bpy.data.meshes.new_from_object(evaluated_obj, depsgraph=depsgraph)

        # Create a bmesh from mesh
        # (won't affect mesh, unless explicitly written back)
        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Bisect to prep for symmetry
        if props.symmetryX or props.symmetryY or props.symmetryZ:
            bisect.bisect_on_axes(bm, props.symmetryX, props.symmetryY, props.symmetryZ)

        mesh_name = os.path.join(bpy.app.tempdir, obj.name)
        mesh_filepath = f"{mesh_name}.obj"
        self.report({'DEBUG'}, f"Remeshing from {mesh_filepath}")

        # Export selected object as OBJ
        export.export_mesh(bm, mesh_filepath)
        # bpy.ops.wm.obj_export(filepath=mesh_filepath, apply_modifiers=True, check_existing=False, export_selected_objects=True, export_materials=False, export_uv=False)

        # Load lib
        qw = Quadwild(mesh_filepath)

        if props.enableSharp:
            # Calculate sharp
            export.export_sharp_features(bm, qw.sharp_path, props.sharpAngle)

        # Remesh and calculate field
        qw.remeshAndField(remesh=props.enableRemesh, enableSharp=props.enableSharp, sharpAngle=props.sharpAngle)
        if props.debug:
            bpy.ops.wm.obj_import(filepath=qw.remeshed_path, check_existing=True, forward_axis="Y", up_axis="Z")

        # Trace
        qw.trace()
        if props.debug:
            bpy.ops.wm.obj_import(filepath=qw.traced_path, check_existing=True, forward_axis="Y", up_axis="Z")

        # Convert to quads
        qw.quadrangulate(
            qr_props.scaleFact,
            qr_props.fixedChartClusters,

            qr_props.alpha,
            qr_props.ilpMethod,
            qr_props.timeLimit,
            qr_props.gapLimit,
            qr_props.minimumGap,
            qr_props.isometry,
            qr_props.regularityQuadrilaterals,
            qr_props.regularityNonQuadrilaterals,
            qr_props.regularityNonQuadrilateralsWeight,
            qr_props.alignSingularities,
            qr_props.alignSingularitiesWeight,
            qr_props.repeatLosingConstraintsIterations,
            qr_props.repeatLosingConstraintsQuads,
            qr_props.repeatLosingConstraintsNonQuads,
            qr_props.repeatLosingConstraintsAlign,
            qr_props.hardParityConstraint,

            qr_props.flowConfig,
            qr_props.satsumaConfig,
        )
        if props.debug:
            bpy.ops.wm.obj_import(filepath=qw.output_path, check_existing=True, forward_axis="Y", up_axis="Z")

        # Import remeshed OBJ
        bpy.ops.wm.obj_import(filepath=qw.output_smoothed_path, check_existing=True, forward_axis="Y", up_axis="Z")
        imported_obj = ctx.selected_objects[0]
        imported_obj.name = f"{obj.name} Remeshed"

        # Add Mirror modifier
        if props.symmetryX or props.symmetryY or props.symmetryZ:
            mirror_modifier = imported_obj.modifiers.new("Mirror", "MIRROR")

            mirror_modifier.use_axis[0] = props.symmetryX
            mirror_modifier.use_axis[1] = props.symmetryY
            mirror_modifier.use_axis[2] = props.symmetryZ
            mirror_modifier.use_clip = True
            mirror_modifier.merge_threshold = 0.001

            # bpy.ops.object.modifier_apply(modifier=mirror_modifier.name)

        # Hide original
        obj.hide_set(True)
        del qw

        # Flush changes from wrapped bmesh / write back to mesh
        # if mesh_obj.mode == 'EDIT':
        #     bmesh.update_edit_mesh(mesh)
        # else:
        #     bm.to_mesh(mesh)
        #     mesh.update()

        bm.free()
        del bm
        evaluated_obj.to_mesh_clear()


        return {'FINISHED'}
