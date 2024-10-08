import bmesh


def export_sharp_features(bm: bmesh.types.BMesh, sharp_filepath: str, sharp_angle: float=35) -> int:
    """Export edges marked sharp, boundary, and seams as sharp features as OBJ format"""

    sharp_edges = []
    bm.edges.index_update()
    bm.edges.ensure_lookup_table()

    for edge in bm.edges:
        if edge.is_wire:
            continue
        if not edge.smooth:
            convexity = 1 if edge.is_convex else 0
            face = edge.link_faces[0]
            face_index = face.index
            for ei, e in enumerate(face.edges):
                if e.index == edge.index:
                    edge_index = ei
                    break
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
        f.write('\n')
        f.close()
