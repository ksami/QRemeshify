import bmesh
import bpy
import math


def export_sharp_features(mesh: bpy.types.Mesh, sharp_filepath: str, sharp_angle: float=35):
    # Create a bmesh from mesh
    # (won't affect mesh, unless explicitly written back)
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Export edges marked sharp, boundary, and seams as sharp features
    sharp_edges = []
    bm.edges.ensure_lookup_table()
    for edge in bm.edges:
        angle_rad = edge.calc_face_angle(0)
        if math.degrees(angle_rad) > sharp_angle:
            edge.smooth = False

        if not edge.smooth or edge.is_boundary or edge.seam:
            convexity = 1 if edge.is_convex else 0
            face_index = edge.link_faces[0].index
            edge_index = edge.index
            sharp_edges.append(f"{convexity},{face_index},{edge_index}")

    num_sharp_features = len(sharp_edges)
    print(f"Found {num_sharp_features} sharp edges")

    with open(sharp_filepath, 'w') as f:
        f.write(f"{num_sharp_features}\n")
        for edge in sharp_edges:
            f.write(f"{edge}\n")
        f.close()

    # Flush changes from wrapped bmesh / write back to mesh
    # if mesh_obj.mode == 'EDIT':
    #     bmesh.update_edit_mesh(mesh)
    # else:
    #     bm.to_mesh(mesh)
    #     mesh.update()

    bm.free()
    del bm
