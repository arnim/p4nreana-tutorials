# Create your custom image!

## About

As we saw in the previous examples, depending on what we need for our analysis we can use different [Docker](https://docs.docker.com/get-started/overview/) images in the `workflow/steps/environment` section of the yaml file; indeed, we used public images from [Docker Hub](https://hub.docker.com/) like `python:3.10-bookworm`, from [Jupyter Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) `jupyter/scipy-notebook`, and custom images we prepared with our preferred libraries `reana-env:py311-astro`.

Now we want to show how to build your own imgage on gitlab, so that you can create the perfect environment for your code to run, as the available ones might not always have all the packages and libraries you need.

## Steps to create a Docker Image on gitlab
### 1. Define the `image` in the .gitlab-ci.yml file

Create a file named **.gitlab-ci.yml** that will contain the image configuration, e.g.:

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

Create a file named **Dockerfile** that will contain the base image and the additional packages you want to install, e.g.:

```
FROM jupyter/scipy-notebook

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```

In this case, all additional libraries are contained in the file **requirements.txt** that is run by `pip`.  
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
Copy the image path and you can now use it, e.g. as a reana environment.

N.B.: it might be necessary to make it public if it's not.


## Useful links
- Intro to Docker: [Docker Crash Course](https://www.youtube.com/watch?v=pg19Z8LL06w&amp;ab_channel=TechWorldwithNana)
- Gitlab Docs: [Docker integration](https://docs.gitlab.com/ee/ci/docker/)
