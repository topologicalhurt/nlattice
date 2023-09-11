import pymesh as pm
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt


def print_wire_data(wn):
    print(f"Dim: {wn.dim}")
    print(f"Vertices: {wn.num_vertices}")
    print(f"Edges: {wn.num_edges}")

def get_wireframe(mesh):
    # You can switch to the legacy impl using get_wire_info_prototype (can remove this later)
    # v, e = get_wire_info_delaunay(mesh)
    v, e = get_wire_info_prototype(mesh)
    return get_wire_info(v, e)


def get_wire_info_prototype(mesh):
    return np.dot(mesh.vertices, 3), mesh.faces

def get_wire_info(vertices, faces):

    edges = []
    check = []
    for f in range(len(vertices)):
        inner = []
        for v in range(len(vertices)):
            inner.append(False)
        check.append(inner)

    for v in range(len(faces)):

        for a in range(len(faces[v])-1):
            x = faces[v][a]
            y = faces[v][a+1]
            if x == y:
                continue
            if check[x][y]:
                continue
            temp = np.array([x, y])
            check[x][y] = True
            check[y][x] = True
            edges.append(temp)

    np_edges = np.array(edges)
    print("EDGES")
    print(np_edges)
    return vertices, np_edges


if __name__ == "__main__":
    mesh = pm.load_mesh("pokemonstl/bulbasaur_starter_1gen_flowalistik.stl")
    # mesh = pm.generate_box_mesh(np.array([0, 0, 0]), np.array([20, 20, 20]), using_simplex=True)
    mesh, __ = pm.collapse_short_edges(mesh, rel_threshold=0.25)
    mesh, info = pm.split_long_edges(mesh, 5)


    print("Vertices, faces, voxels")
    print(mesh.num_vertices, mesh.num_faces, mesh.num_voxels)
    print("dim, vertex_per_face, vertex_per_voxel")
    print(mesh.dim, mesh.vertex_per_face, mesh.vertex_per_voxel)

    # tol = 2.0
    # mesh, info = pm.collapse_short_edges(mesh, tol)
    # print(info["num_edge_collapsed"])

    # o_vertices, o_edges = get_wire_info(mesh)


    vertices, edges = get_wireframe(mesh)
    wire_network = pm.wires.WireNetwork.create_from_data(vertices, edges)

    print_wire_data(wire_network)
    # Inflator
    inflator = pm.wires.Inflator(wire_network)
    inflator.inflate(0.2)
    mesh = inflator.mesh

    # save the mesh
    pm.save_mesh("bulbasaur_demo.stl", mesh)
