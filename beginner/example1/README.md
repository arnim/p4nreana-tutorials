# "Hello World!"

[![Launch on REANA](https://www.reana.io/static/img/badges/launch-on-reana.svg)]($https://reana-p4n.aip.de/launch?name=helloworld&url=https%3A%2F%2Fgitlab-p4n.aip.de%2Fp4nreana%2Ftutorials%2F-%2Ftree%2Fmain%2Fbeginner%2Fexample1)

## About
This example prints a simple "hello world" message through REANA.

## Structure
We will address (1) the source code, (2) which computing environments were used to run the software, and (3) which computational steps are needed to run the code.

### 1. Source code
The simplest "hello world" Python code saved in **helloworld.py**:  
`print("Hi from Reana!")`

### 2. Environment
In order to be able to rerun the analysis even several years in the future, we need to "encapsulate" the current computing environment, for example to freeze the library versions that our analysis was using. We can achieve this through a Docker container image.  
Since we don't need any additional Python packages for this simple example to work, we can directly rely on the python image from the Docker Hub, in this case `python:3.10-bookworm`.

### 3. Workflow
For this example to run, we just need to execute the python code contained in the file:  
`python helloworld.py`

## Running the example on REANA
This is a step-by-step guide on how to use the REANA command-line client to launch this analysis example.
We start by creating a **reana.yaml** file describing the above analysis structure with its inputs, code, runtime environment, and computational workflow steps:

```
inputs:
  files:
    - helloworld.py
workflow:
  type: serial
  specification:
    steps:
      - environment: 'docker.io/library/python:3.10-bookworm'
        commands:
        - python helloworld.py
```

In this example we only have the source code file as input, and we are using a simple Serial workflow engine to represent our sequential computational workflow steps.  
The environment is specified as discussed, as well as the only command to execute.

After installing the REANA command-line client (see the **instructions** [here](https://gitlab-p4n.aip.de/p4nreana/tutorial2023/-/blob/main/README.md)), we can run the example:

```
$ # test connection
$ reana-client ping
$ # check if reana.yaml is correct
$ reana-client validate
$ # create new workflow
$ reana-client create -n hello
$ # set the environment variable
$ export REANA_WORKON=hello
$ # upload input code and workflow (yaml file) to the workspace
$ reana-client upload
$ # start workflow
$ reana-client start
$ # check the job stauts (should be finished quickly)
$ reana-client status
$ # check logs and output
$ reana-client logs
```

Please see the [REANA-Client](https://reana-client.readthedocs.io/) documentation for more detailed explanation of typical `reana-client` usage scenarios.  
Also useful is the [reana.yaml](https://docs.reana.io/reference/reana-yaml/) documentation.
