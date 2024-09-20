import bmesh
import math


def export_sharp_features(bm: bmesh.types.BMesh, sharp_filepath: str, sharp_angle: float=35) -> int:
    """Export edges marked sharp, boundary, and seams as sharp features as OBJ format"""

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
    with open(sharp_filepath, 'w') as f:
        f.write(f"{num_sharp_features}\n")
        for edge in sharp_edges:
            f.write(f"{edge}\n")
        f.close()

    return num_sharp_features


def export_mesh(bm: bmesh.types.BMesh, mesh_filepath: str) -> None:
    """Export mesh as OBJ format"""

    verts = []
    vert_normals = []
    faces = []

    for v in bm.verts:
        verts.append(f"v {v.co.x:.6f} {v.co.y:.6f} {v.co.z:.6f}")

    for fid, f in enumerate(bm.faces):
        # NOTE: Blender will export per face normals if flat-shaded, per face per loop normals if smooth-shaded
        vert_normals.append(f"vn {f.normal.x:.4f} {f.normal.y:.4f} {f.normal.z:.4f}")

        face_verts = []
        for v in f.verts:
            # NOTE: OBJ indices start at 1
            face_verts.append(f"{v.index + 1}//{fid + 1}")

        faces.append(f"f {' '.join(face_verts)}")


    with open(mesh_filepath, 'w') as f:
        f.write("# OBJ file\n")
        f.write('\n'.join(verts))
        f.write('\n')
        f.write('\n'.join(vert_normals))
        f.write('\n')
        f.write('\n'.join(faces))
        f.close()
