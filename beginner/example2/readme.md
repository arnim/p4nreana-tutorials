 ## REANA example - "sinefunction
 -----
 

 ### About
 ----
 This repository provides a simple "sine function" application example for [REANA](https://www.reanahub.io/) reusable research data analysis platform.
 
 ### Structure
 ---
 
To run a REANA workflow, you typically need the following files:
#### 1. **Source code**

To create a simple "sine function" application example for a REANA reusable research data analysis platform, you can use this Python script saved as ```sine_plot.py ```

#### 2. **Environment Requirements**
It's important to choose an environment that includes all the necessary dependencies for the specific task at hand. The custom environments are needed, you can create your own Docker images and use them in the environment specification. Here we have used our own dokcer images from gitlab 
`gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro.10125`.

#### 3. **Workflow Specification (YAML)**:
This file describes the structure and steps of your workflow. It includes information about input data, steps to be executed, and any necessary parameters. The default name is often **workflow.yaml**.

``` 
version: 0.9.0
inputs:
  files:
    - sine_plot.py
outputs:
  directories:
    - output
workflow:
  type: serial
  specification:
    steps:
      - name: run-sine_plot
        environment: 'gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro.10125'
        commands:
          - python sine_plot.py
```

To run:

```
$ # test the connection
$ reana-client ping
$ # create a  new workflow
$ reana-client create -n sin
$ # set the reana environment variable
$ export REANA_WORKON=sin
$ # upload input code and workflow to the workspace
$ reana-client upload
$ # start the workflow
$ reana-client start
$ # check workflow status
$ reana-client status
$ # check logs and output
$ reana-client logs


```
