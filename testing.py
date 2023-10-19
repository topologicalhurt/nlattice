from meshlib import mrmeshpy as mm
from meshlib import mrmeshnumpy as mn
import numpy as np
import plotly.graph_objects as go


def visualise(mesh):
    verts = mn.getNumpyVerts(mesh)
    faces = mn.getNumpyFaces(mesh.topology)

    vertsT = np.transpose(verts)
    facesT = np.transpose(faces)

    m = mesh.volume

    fig = go.Figure(data=[
        go.Mesh3d(
            x=vertsT[0],
            y=vertsT[1],
            z=vertsT[2],
            i=facesT[0],
            j=facesT[1],
            k=facesT[2]
        )
    ])

    fig.show()


if __name__ == "__main__":
    mesh = mm.loadMesh(mm.Path("pokemonstl/totodile_demo.stl"))
    # mesh = mm.loadMesh(mm.Path("pokemonstl/example1.mesh"))
    visualise(mesh)


