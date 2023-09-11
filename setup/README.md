# How to run


## Macbook

1. Download Docker (if you don't have)
2. Pull the PyMesh image
   `docker pull pymesh/pymesh`
3. Build the custom docker image:
    `docker build -t custom_pymesh .`
4. Run the docker image (The following run is due to my Mac AMD64 architecture):
   `docker run --platform linux/amd64 -it --rm -v $(pwd):/local custom_pymesh python /local/setup.py`