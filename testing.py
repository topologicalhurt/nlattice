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

def visualise(mesh, edge_size, tess_size):
    verts = mn.getNumpyVerts(mesh)
    faces = mn.getNumpyFaces(mesh.topology)

    #Scale the vertices based on tessellation size
    verts = verts * tess_size

    vertsT = np.transpose(verts)
    facesT = np.transpose(faces)

    m = mesh.volume

    fig = go.Figure(data=[
        go.Mesh3d(
            #Modify edge_size and tess_size to scale the mesh
            x=vertsT[0],
            y=vertsT[1],
            z=vertsT[2],
            i=facesT[0],
            j=facesT[1],
            k=facesT[2],
        )
    ])

    fig.update_layout(scene=dict(bgcolor='white'))  # Change background color to white
    return fig

def main():
    st.title("Mesh Visualisation")

    # Custom CSS to make all buttons the same size
    st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            height: 60px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Left column
    left_col, right_col = st.columns([2,1])  # Adjust the ratio of the columns

    with left_col:
        st.subheader("Tessellation")  # Change to subheader for smaller text
        col_1, col_2 = st.columns([1, 1])  # Create two columns side by side
        with col_1:
            if st.button("Kagome"):
                st.write("Kagome selected")
            if st.button("Tetrahedral"):
                st.write("Tetrahedral selected")
            if st.button("Icosahedral"):
                st.write("Icosahedral selected")
            if st.button("Voronoi"):
                st.write("Voronoi selected")
            if st.button("Rhombic"):
                st.write("Rhombic selected")

        st.subheader("Node placement algorithm")  # Change to subheader for smaller text
        col1, col2 = st.columns([1, 1])  # Create two columns side by side
        with col1:
            if st.button("Delaunay Triangulation"):
                st.write("Delaunay Triangulation selected")
            if st.button("Voronoi Triangulation"):
                st.write("Voronoi Triangulation selected")

        with col2:
            if st.button("Minimum Weight Triangulation"):
                st.write("Minimum Weight Triangulation selected")
            if st.button("Bowyer-Watson Triangulation"):
                st.write("Bowyer-Watson Triangulation selected")

        #Slider for edge size
        edge_size = st.slider("Edge size", min_value=0.0, max_value=10.0, value=1.0)
        #Slider for tessellation size
        tess_size = st.slider("Tessellation size", min_value=0.0, max_value=10.0, value=1.0)
        #Create convert button
        if st.button("Convert"):
            st.write("Converted!")
            # #Load the mesh
            # mesh = mm.loadMesh(mm.Path("pokemonstl/bulbasaur_demo.stl"))
            # #Modify mesh using edge_size and tess_size
            # mesh = mm.modifyMesh(mesh, edge_size)
            # mesh = mm.modifyMesh(mesh, tess_size)
            # #Visualise the mesh
            # fig = visualise(mesh, edge_size, tess_size)
            # with right_col:
            #     st.header("Converted Mesh")
            #     st.plotly_chart(fig)
            # st.write("Converted!")

    # Right column
    with right_col:
        st.header("Mesh")
        mesh = mm.loadMesh(mm.Path("pokemonstl/bulbasaur_demo.stl"))
        fig = visualise(mesh, edge_size, tess_size)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()

