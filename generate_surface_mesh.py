import pymesh as pm
import numpy as np
import matplotlib.pyplot as plt
import sys
import numpy as np


def plot_points_plt(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Points Before Delaunay Triangulation')
    plt.savefig("test_point_interior.png", dpi=150)


def print_wire_data(wn):
    print(f"Dim: {wn.dim}")
    print(f"Vertices: {wn.num_vertices}")
    print(f"Edges: {wn.num_edges}")


def get_required_triangle_form(mesh):
    vertices = mesh.vertices
    faces = mesh.faces
    outer = []
    for i in range(len(faces)):
        points = []
        for j in range(len(faces[i])):
            v = faces[i][j]
            points.append(vertices[v])
        point_np = np.array(points)
        outer.append(point_np)
    outer_np = np.array(outer)
    print(outer_np.shape)
    return outer_np


def get_wireframe(mesh):
    v, f = get_wire_info_prototype(mesh)
    return get_wire_info(v, f)


def get_wire_info_prototype(mesh):
    return np.dot(mesh.vertices, 1), mesh.faces


def edges_from_faces(vertices, faces):
    edges = []
    check = []
    # check is to ensure we don't double up
    for f in range(len(vertices)):
        inner = []
        for v in range(len(vertices)):
            inner.append(False)
        check.append(inner)

    for v in range(len(faces)):

        for a in range(len(faces[v])):
            if a >= len(faces[v]) - 1:
                x = faces[v][0]
                y = faces[v][a]
            else:
                x = faces[v][a]
                y = faces[v][a + 1]
            if x == y:
                continue
            if check[x][y]:
                continue
            temp = np.array([x, y])
            check[x][y] = True
            check[y][x] = True
            edges.append(temp)
    return np.array(edges)


def get_wire_info(vertices, faces):
    # switching to the wrapper of si's tetgen library to try and get tetrahedral voxels of the object
    tet = pm.tetgen()
    tet.points = vertices
    tet.triangles = faces
    # tet.keep_convex_hull = True
    tet.max_tet_volume = 180
    tet.min_dihedral_angle = 15.0
    tet.verbosity = 1
    tet.run()
    new_mesh = tet.mesh
    faces = new_mesh.voxels
    vertices = new_mesh.vertices

    np_edges = edges_from_faces(vertices, faces)

    return vertices, np_edges


def parse_args():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    wire_thickness = sys.argv[2] if len(sys.argv) > 2 else None
    longest_line = sys.argv[3] if len(sys.argv) > 3 else None

    if file_path is None or wire_thickness is None or longest_line is None:
        print("Usage: python generate_surface_mesh.py <filepath> <wire thickness> <longest edge>")
        exit()

    else:
        return file_path, float(wire_thickness), float(longest_line)


if __name__ == "__main__":
    path, thickness, longest_line = parse_args()
    mesh = pm.load_mesh(path)
    # Generate box for testing below
    box_mesh = pm.generate_box_mesh(np.array([0, 0, 0]), np.array([5, 5, 5]), using_simplex=True)
    mesh, __ = pm.collapse_short_edges(mesh, rel_threshold=0.30)
    # mesh, info = pm.split_long_edges(mesh, longest_line)

    print("Vertices, faces, voxels")
    print(mesh.num_vertices, mesh.num_faces, mesh.num_voxels)
    print("dim, vertex_per_face, vertex_per_voxel")
    print(mesh.dim, mesh.vertex_per_face, mesh.vertex_per_voxel)

    # interior_points = generate_interior_points(mesh, longest_line)
    # plot_points_plt(interior_points)

    vertices, edges = get_wireframe(mesh)
    wire_network = pm.wires.WireNetwork.create_from_data(vertices, edges)

    print_wire_data(wire_network)
    wire_network.trim()
    # Inflator
    inflator = pm.wires.Inflator(wire_network)
    # inflator.set_refinement(2, "loop")
    inflator.inflate(thickness, allow_self_intersection=True)
    mesh = inflator.mesh

    print("inflated, saving now")
    # save the mesh
    pm.save_mesh("point_test_demo180trimmed.stl", mesh)
