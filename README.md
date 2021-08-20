# berkeley-interact

Python module to run the (legacy) Berkeley PCFG Parser interactively using the 
[berkeleyinterface](https://github.com/btibs/berkeleyinterface) package wrapped using
`Flask` to provide a server that can be queried using `GET` requests.

## Usage

Send a GET request within your script, using `curl`, or a service such as 
[`postman`](https://www.postman.com/downloads/?utm_source=postman-home).
```bash
GET localhost:8000/default 
  {
    "sentence": "This is an example sentence to be parsed"
  }
```
The request above returns a response containing the parse tree of the supplied sentence
using the default English grammar distributed with the parser.
``

To use a specific grammar (currently available: [GCG-15 (Nguyen, Schijndel, & Schuler, 2012)](https://aclanthology.org/C12-1130.pdf)), 
use the appropriate endpoint: `localhost:8000/fullberk`, or simply pass it as a parameter in your query (`NotImplemented`).
E.g., 
```bash
GET localhost:8000/fullberk 
  {
    "sentence": "This is an example sentence to be parsed"
  }
```
The request above produces the following response: ``.

## Installation

### Preferred way: Docker

We highly recommend using a container to run the program.
You may either use `docker` to [build an image](https://docs.docker.com/engine/reference/commandline/build/) 
using the `Dockerfile` in the repository:
```bash
sudo docker build -t <your_preferred_image_name> .
```
Or use a pre-built image from Docker hub, [`aloxatel/berkeleyparser`](https://hub.docker.com/repository/docker/aloxatel/berkeleyparser).

Then run the image inside a container using your choice of a container daemon (e.g., `docker`, `singularity`).
Here's an example using `docker`:
```bash
sudo docker run -it --net=host --expose 8000 -p 8000:8000 aloxatel/berkeleyparser:latest
```
This command will create a container and spawn a server within the container, binding the port `8000`
to the same port on the `host` machine.

