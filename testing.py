# from meshlib import mrmeshpy as mm
# from meshlib import mrmeshnumpy as mn
# import numpy as np
# import plotly.graph_objects as go


# def visualise(mesh):
#     verts = mn.getNumpyVerts(mesh)
#     faces = mn.getNumpyFaces(mesh.topology)

#     vertsT = np.transpose(verts)
#     facesT = np.transpose(faces)

#     m = mesh.volume

#     fig = go.Figure(data=[
#         go.Mesh3d(
#             x=vertsT[0],
#             y=vertsT[1],
#             z=vertsT[2],
#             i=facesT[0],
#             j=facesT[1],
#             k=facesT[2]
#         )
#     ])

#     fig.show()


# if __name__ == "__main__":
#     mesh = mm.loadMesh(mm.Path("pokemonstl/bulbasaur_demo.stl"))
#     # mesh = mm.loadMesh(mm.Path("pokemonstl/example1.mesh"))
#     visualise(mesh)

import streamlit as st
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

    fig.update_layout(scene=dict(bgcolor='white'))  # Change background color to white
    return fig

def main():
    st.title("Mesh Visualisation")

    # Left column
    left_col, right_col = st.columns([2,1])  # Adjust the ratio of the columns

    with left_col:
        st.subheader("Tessellation")  # Change to subheader for smaller text
        if st.button("Kagome"):
            st.write("Kagome selected")
        if st.button("Tetrahedral"):
            st.write("Tetrahedral selected")

        st.subheader("Node placement algorithm")  # Change to subheader for smaller text
        col1, col2 = st.columns([1, 1])  # Create two columns side by side
        if col1.button("Delaunay Triangulation !"):
            st.write("Delaunay Triangulation selected")
        if col2.button("Minimum weight Triangulation !"):
            st.write("Minimum weight Triangulation selected")

    # Right column
    with right_col:
        st.header("Mesh")
        mesh = mm.loadMesh(mm.Path("pokemonstl/bulbasaur_demo.stl"))
        fig = visualise(mesh)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()

