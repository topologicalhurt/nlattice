# nlattice
The objective of this project is to develop a program to process a 3D object in surface triangle mesh format (STL file) and generate a valid STL file of a lattice object representing the same form as the input. 

# Setup:

This project runs a modified version of the public pymesh docker image. The first steps are almost identical to https://github.com/PyMesh/PyMesh/blob/main/README.md

This guide additionally assumes that the root folder will be built at ```~/Documents/pymesh``` and it also assumes that docker is installed https://docs.docker.com/get-docker/


```
cd ~/Documents
mkdir pymesh
cd pymesh
```

If you have not done so already download **test_model.stl** from the repository and place it in the **pymesh** folder

## In windows:

```
start PowerShell {docker run -it pymesh/pymesh; Read-Host}
start PowerShell {docker exec -it $(docker ps -q) /bin/bash; Read-Host}
```

## In linux:

```
```
