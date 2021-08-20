# berkeley-interact

Python module to run the (legacy) Berkeley PCFG Parser as a server.
We utilize the 
[berkeleyinterface](https://github.com/btibs/berkeleyinterface) package and wrap
it in a `Flask` app to provide a barebones server that can be queried using `GET` requests.

## Usage: How to interact with it

Send a GET request within your script, using `curl`, or a service such as 
[`postman`](https://www.postman.com/downloads/?utm_source=postman-home).
```bash
curl --location --request GET 'localhost:8000/default' \
     --header 'Content-Type: application/json' \
     --data-raw '{
        "sentence": "This is an example sentence to be parsed."
     }'
```
The request above returns a response containing the parse tree of the supplied sentence
using the default English grammar distributed with the parser. 
Here is the server-side log (takes a bit longer on first request due to loading the grammar, but subsequent requests are executed rapidly):
```
==== INFO @ 0.00 attempting to start up the parser JVM using ./bin/BerkeleyParser-1.7.jar
==== INFO @ 0.05 ---done--- starting up the parser JVM
==== INFO @ 3.58 lightweight parser received sentence: This is an example sentence to be parsed.
==== INFO @ 3.69 loading the grammar ./bin/eng_sm6.gr
==== INFO @ 12.55 ---done--- loading the grammar
==== INFO @ 12.87 ---done--- lightweight parser produced the following tree: ( (S (NP (DT This)) (VP (VBZ is) (NP (NP (DT an) (NN example) (NN sentence)) (SBAR (S (VP (TO to) (VP (VB be) (VP (VBN parsed)))))))) (. .)) )
```
And here is the output received over http: `( (S (NP (DT This)) (VP (VBZ is) (NP (NP (DT an) (NN example) (NN sentence)) (SBAR (S (VP (TO to) (VP (VB be) (VP (VBN parsed)))))))) (. .)) )`


To use a specific grammar (currently available: [GCG-15 (Nguyen, van Schijndel, & Schuler, 2012)](https://aclanthology.org/C12-1130.pdf)), 
use the appropriate endpoint: `localhost:8000/fullberk`, or simply pass it as a parameter in your query (`NotImplemented`).
E.g., 
```bash
curl --location --request GET 'localhost:8000/fullberk' \
     --header 'Content-Type: application/json' \
     --data-raw '{
        "sentence": "This is an example sentence to be parsed."
     }'
```
The request above produces the following server-side log (takes 5-8 min to load grammar on first run; subsequent requests are executed rapidly):
```
```
And here's the output received over http: ``

## Setup: How to get it up and running

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
to the same port on the `host` machine. In case it doesn't recognize the entrypoint i.e., 
does not spawn the server as anticipated, simply run:
```bash
gunicorn interactive:app --timeout 600
```
Make sure to allow sufficient `--timeout`, at least 600s (10 min), since it takes long to load the GCG-15 grammar on the first run.
If your server times out despite this, try increasing the timeout in 120s increments.