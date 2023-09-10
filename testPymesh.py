import pymesh as pm
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

def delaunay_wireframe(mesh):
    points = mesh.vertices
    tri = Delaunay(points)

    # Below code is to display with matplotlib
    # Plot points
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(points[:, 0], points[:, 1], points[:, 2])

    # Plot Delaunay triangulation wireframe
    # ax.plot_trisurf(points[:, 0], points[:, 1], points[:, 2], triangles=tri.simplices, edgecolor='black', linewidth=0.2,
    #                 alpha=0.1)

    # plt.show()
    return tri


def print_wire_data(wn):
    print(f"Dim: {wn.dim}")
    print(f"Vertices: {wn.num_vertices}")
    print(f"Edges: {wn.num_edges}")


def get_wire_info(mesh):
    vertices = np.dot(mesh.vertices, 3)

    faces = mesh.faces

    # getting edges
    # mesh.enable_connectivity() csdf
    edges = []
    check = []
    for f in range(len(vertices)):
        inner = []
        for v in range(len(vertices)):
            inner.append(False)
        check.append(inner)

    for v in range(len(faces)):

       #  print(v, adjacent)
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
    print(np_edges)
    return vertices, np_edges


if __name__ == "__main__":
    mesh = pm.load_mesh("pokemonstl/bulbasaur_starter_1gen_flowalistik.stl")
    # mesh = pm.generate_box_mesh(np.array([0, 0, 0]), np.array([20, 20, 20]), using_simplex=True)
    print("Vertices, faces, voxels")
    print(mesh.num_vertices, mesh.num_faces, mesh.num_voxels)
    print("dim, vertex_per_face, vertex_per_voxel")
    print(mesh.dim, mesh.vertex_per_face, mesh.vertex_per_voxel)

    # tol = 2.0
    # mesh, info = pm.collapse_short_edges(mesh, tol)
    # print(info["num_edge_collapsed"])

    # o_vertices, o_edges = get_wire_info(mesh)
    """
    tetgen = pm.tetgen()
    tetgen.points = o_vertices
    tetgen.triangles = mesh.faces
    tetgen.max_tet_volume = 0.1
    tetgen.verbosity = 0
    tetgen.run()
    new_mesh = tetgen.mesh
    """

    vertices, edges = get_wire_info(mesh)
    wire_network = pm.wires.WireNetwork.create_from_data(vertices, edges)

    # printing some data
    print_wire_data(wire_network)
    # wire_network.trim()
    # print_wire_data(wire_network)

    # Inflator
    inflator = pm.wires.Inflator(wire_network)
    inflator.inflate(0.2)
    mesh = inflator.mesh

    # save the mesh
    pm.save_mesh("bulbasaur_demo.stl", mesh)
