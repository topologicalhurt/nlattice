# nlattice
The objective of this project is to develop a program to process a 3D object in surface triangle mesh format (STL file) and generate a valid STL file of a lattice object representing the same form as the input. 

# Setup:

This project runs a modified version of the public pymesh docker image. The first steps are almost identical to https://github.com/PyMesh/PyMesh/blob/main/README.md

This guide additionally assumes that the root folder will be built at ```~/Documents/pymesh``` and it also assumes that docker is installed https://docs.docker.com/get-docker/


```
cd ~/Documents
mkdir pymesh
cd pymesh
wget -O setup.tar https://github.com/topologicalhurt/nlattice/raw/main/setup.tar
```

__> ℹ️ You may also want to consider creating the test_model_setup.py to get used to using emacs in an SSH session shell. More info later in the guide on this.__

> [!WARNING]
> Also ensure that you do not create a docker container in-between running commands as ```docker ps <args> -l``` is the first container on the creation stack.

## 🪟 WINDOWS:

```
docker run -it -d pymesh/pymesh
$CONTAINER_ID = docker ps -q -l
docker cp setup.tar "$($CONTAINER_ID):/root/models"
docker exec -it $CONTAINER_ID /bin/bash
cd models
tar -xf setup.tar & rm setup.tar
```

From here it is valid to run: ```cd setup & python3 setup.py``` but the image comes with an unupdated python environment variable which we will now fix (this is a slightly modified version of this helpful guide here https://aruljohn.com/blog/install-python-debian/):

```
apt update
cd /tmp/
wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz
tar -xzvf Python-3.11.4.tgz
cd Python-3.11.4
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
./configure --enable-optimizations
make -j `nproc`
make install
```

When you run ```python3 -v``` it should now return ```Python 3.11.4```

Now run:

```
cd /root/models/setup
python3 setup.py
```

The program should successfully display the number of vertices, faces & edges.

If you would like some experience getting used to emacs:

```
apt-get install emacs
touch setup.py
emacs setup.py
```
