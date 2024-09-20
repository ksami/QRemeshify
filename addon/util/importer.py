import bpy
import os


def import_mesh(mesh_filepath: str) -> bpy.types.Mesh:
    if not os.path.isfile(mesh_filepath):
        raise Exception(f"File does not exist at {mesh_filepath}")

    with open(mesh_filepath, 'r') as f:
        lines = f.read().splitlines()
        f.close()

    verts = []
    edges = []
    faces = []

    for line in lines:
        tokens = line.split(' ')
        element = tokens[0]

        if element == 'v':
            verts.append(tuple([float(coord) for coord in tokens[1:]]))
        elif element == 'f':
            # NOTE: OBJ indices start at 1
            faces.append(tuple([int(vertex_id) - 1 for vertex_id in tokens[1:]]))
        else:
            continue

    new_mesh = bpy.data.meshes.new('Mesh')
    new_mesh.from_pydata(verts, edges, faces)
    new_mesh.update()

    return new_mesh
