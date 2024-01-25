# Create your custom image!

[Docker](https://docs.docker.com/get-started/overview/) is an open platform for developing, shipping, and running applications. A Docker image is a read-only template with instructions for creating a Docker container, where the application will run. Often, an image is based on another image, with some additional customization.

## About

As we saw in the previous examples, depending on what we need for our analysis we can use different Docker images in the `workflow/steps/environment` section of the yaml file; indeed, we used public images from [Docker Hub](https://hub.docker.com/) like `python:3.10-bookworm`, from [Jupyter Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) `jupyter/scipy-notebook`, and custom images we prepared with our preferred libraries `reana-env:py311-astro` (see [this example](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/intermediate/example2)).

Now we want to show how to build your own imgage on gitlab, so that you can create the perfect environment for your code to run, as the available ones might not always have all the packages and libraries you need.

## Steps to create a Docker Image on gitlab
### 1. Define the `image` in the .gitlab-ci.yml file

Create a file named **.gitlab-ci.yml** that will contain the image configuration. Specifically, we need some GitLab [variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html) decribing, e.g., the image name and tag, that will be composed by:
- `$CI_REGISTRY_IMAGE`: the address of the project’s Container Registry (in this case the gitlab repository where we are building the image, e.g., gitlab-p4n.aip.de:5005/p4nreana/reana-env)
- `$CI_COMMIT_REF_SLUG`: the branch or tag name where the project is built (e.g., py311-astro)
- `$CI_JOB_ID`: a serial number with the image version (e.g., 9845)

Then we need to actually build the image, by specifying the following steps in the section `build-push-docker-image-job`:
- `image`: a Docker image to run the job in
- `services`: additional services needed to run the job
- `before_script`: commands that should run before each job’s script commands
- `script`: run all the commands to create the image

This is an example of this file, that you can use as it is:

```
variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG.$CI_JOB_ID
  
build-push-docker-image-job:
  # Specify a Docker image to run the job in.
  image: docker:20.10.16
  # Specify an additional image 'docker:dind' ("Docker-in-Docker") that
  # will start up the Docker daemon when it is brought up by a runner.
  services:
    - docker:20.10.16-dind
  before_script:
    - docker info
  script:
    - export 
    - ls -latr
    - echo  $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER $CI_REGISTRY --password-stdin
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
```

### 2. Create a Dockerfile

Create a new file and name it **Dockerfile**; it will contain the base image and the additional packages you want to install. First, you need to specify a base image, with the command `FROM`, e.g. from a public repository. Then you can upload the needed files with `COPY`, like a requirements file containing all the packages and libraries you need to install. Finally, with `RUN` you specify the commands to install everything on top of the base image (e.g. `pip`).

This is a very simple example of a Dockerfile, where we install the python libraries specified inside **requirements.txt** on top of a base image available [here](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html):

```
FROM jupyter/scipy-notebook

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```

In this case, all additional libraries are contained in the file **requirements.txt** that is run by `pip`. If you need specific versions of these libraries, you can add the version number, e.g. `numpy>=1.23.1`.  
This file need to be created and it will be something like:

```
scipy
numpy
pandas
matplotlib
astropy
seaborn
papermill
plotly
pyvo
bokeh
pyviz_comms
hvplot
holoviews
dask
distributed
scikit-learn
tensorflow
datashader
```

### 3. Check CI/CD is turned on

On the side bar, go to `settings > CI/CD > Runners`, expand and check that there is a runner enabled for the project. If not, enable it.

Wait until the pipeline finishes running, and if successful your image is created!

### 4. Use your new image

Go to `Deploy > Container registry` and you should see a new tag with the name you defined and a version number.  
Copy the image path and you can now use it as, e.g., a reana environment.

N.B.: it might be necessary to make it public if it's not.


## Useful links
- Intro to Docker: [Docker Crash Course](https://www.youtube.com/watch?v=pg19Z8LL06w&amp;ab_channel=TechWorldwithNana)
- Gitlab Docs: [Docker integration](https://docs.gitlab.com/ee/ci/docker/)
