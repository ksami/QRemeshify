import bmesh
import bpy
import mathutils
import os
from .lib import Quadwild
from .util import bisect, exporter, importer


class QREMESH_OT_Remesh(bpy.types.Operator):
    """Remesh with Quadwild"""
    bl_idname = "qremeshify.remesh"
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

        mesh_name = os.path.join(bpy.app.tempdir, obj.name)
        mesh_filepath = f"{mesh_name}.obj"
        self.report({'DEBUG'}, f"Remeshing from {mesh_filepath}")

        # Load lib
        qw = Quadwild(mesh_filepath)

        if not props.useCache:
            # Get mesh after modifiers and shapekeys applied
            depsgraph = bpy.context.evaluated_depsgraph_get()
            evaluated_obj = obj.evaluated_get(depsgraph)
            mesh = evaluated_obj.to_mesh()

            # Create a bmesh from mesh
            # (won't affect mesh, unless explicitly written back)
            bm = bmesh.new()
            bm.from_mesh(mesh)

            # Apply only rotation and scale
            if evaluated_obj.rotation_mode == 'QUATERNION':
                matrix = mathutils.Matrix.LocRotScale(None, evaluated_obj.rotation_quaternion, evaluated_obj.scale)
            else:
                matrix = mathutils.Matrix.LocRotScale(None, evaluated_obj.rotation_euler, evaluated_obj.scale)
            bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)

            # Bisect to prep for symmetry
            if props.symmetryX or props.symmetryY or props.symmetryZ:
                bisect.bisect_on_axes(bm, props.symmetryX, props.symmetryY, props.symmetryZ)

            # Export selected object as OBJ
            exporter.export_mesh(bm, mesh_filepath)

            # Calculate sharp features
            if props.enableSharp:
                num_sharp_features = exporter.export_sharp_features(bm, qw.sharp_path, props.sharpAngle)
                self.report({'DEBUG'}, f"Found {num_sharp_features} sharp edges")

            # Remesh and calculate field
            qw.remeshAndField(remesh=props.enableRemesh, enableSharp=props.enableSharp, sharpAngle=props.sharpAngle)
            if props.debug:
                new_mesh = importer.import_mesh(qw.remeshed_path)
                new_obj = bpy.data.objects.new(f"{obj.name} remeshAndField", new_mesh)
                bpy.context.collection.objects.link(new_obj)
                new_obj.hide_set(True)

            # Trace
            qw.trace()
            if props.debug:
                new_mesh = importer.import_mesh(qw.traced_path)
                new_obj = bpy.data.objects.new(f"{obj.name} trace", new_mesh)
                bpy.context.collection.objects.link(new_obj)
                new_obj.hide_set(True)

        # Convert to quads
        qw.quadrangulate(
            props.enableSmoothing,
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

            qr_props.callbackTimeLimit,
            qr_props.callbackGapLimit,
        )
        if props.debug and props.enableSmoothing:
            new_mesh = importer.import_mesh(qw.output_path)
            new_obj = bpy.data.objects.new(f"{obj.name} quadrangulate", new_mesh)
            bpy.context.collection.objects.link(new_obj)
            new_obj.hide_set(True)

        # Import final OBJ
        final_mesh_path = qw.output_smoothed_path if props.enableSmoothing else qw.output_path
        final_mesh = importer.import_mesh(final_mesh_path)
        final_obj = bpy.data.objects.new(f"{obj.name} Remeshed", final_mesh)
        bpy.context.collection.objects.link(final_obj)
        bpy.context.view_layer.objects.active = final_obj
        final_obj.select_set(True)

        # Add Mirror modifier for symmetry
        if props.symmetryX or props.symmetryY or props.symmetryZ:
            mirror_modifier = final_obj.modifiers.new("Mirror", "MIRROR")

            mirror_modifier.use_axis[0] = props.symmetryX
            mirror_modifier.use_axis[1] = props.symmetryY
            mirror_modifier.use_axis[2] = props.symmetryZ
            mirror_modifier.use_clip = True
            mirror_modifier.merge_threshold = 0.001

        # Hide original
        obj.hide_set(True)

        # Cleanup
        del qw

        if not props.useCache:
            bm.free()
            del bm
            evaluated_obj.to_mesh_clear()


        return {'FINISHED'}
