# REANA Tutorial 2024

## About
[REANA](http://www.reana.io/) is a reusable and reproducible research data
analysis platform. It helps researchers to structure their input data, analysis
code, containerised environments and computational workflows so that the
analysis can be instantiated and run on remote compute clouds.

REANA was born to target the use case of particle physics analyses, but is
applicable to any scientific discipline. The system paves the way towards
reusing and reinterpreting preserved data analyses even several years after the
original publication.

## Getting started
### Install Miniconda
You can skip this if you have already one.
Install conda first:
* Linux:
```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o  Miniconda3-latest-Linux-x86_64.sh
```
* MacOS(x86):
```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o Miniconda3-latest-MacOSX-x86_64.sh
```
* MacOS (M1):
```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o Miniconda3-latest-MacOSX-arm64.sh
```
These commands download the Miniconda installer script for your platform. After downloading, you can proceed with the installation.

*****

Run it and follow the instructions:
```
bash ~/Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
```

Initialize conda:
```
~/miniconda/bin/conda init bash
```

### Prepare a new enviroment
Create a new conda enviroment:
```
conda create -n reana python=3.11
```

Activate it:
```
conda activate reana
```

If you want to automatically activate the reana environment each time you open a terminal, add this line to your  **.bashrc_profile**.

### Install reana-client

```
pip install reana-client

```

### Final steps

We assume that you have already registered on [https://reana-p4n.aip.de](https://reana-p4n.aip.de).  
Login and add into your **$HOME/.bashrc_profile** the credentials from **https://reana-p4n.aip.de/profile**:

```
nano $HOME/.bashrc_profile
```

```
export REANA_SERVER_URL=https://reana-p4n.aip.de
export REANA_ACCESS_TOKEN=XXXXX
```
save, logout and login again into the terminal.

### Testing Setup

```
reana-client ping
```
Result should be something like this:
```
(reana) ~$ reana-client ping
REANA server: https://reana-p4n.aip.de
REANA server version: 0.9.1
REANA client version: 0.9.1
Authenticated as: XXX XXXX
Status: Connected
(reana) ~$
```

## Examples in the Tutorial

### Beginner

1. [Hello World!](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/beginner/example1) -- This example prints a simple "hello world" message through REANA.
2. [Sine plot](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/beginner/example2) -- This example shows how to create a very basic plot of a sine function.

### Intermediate

1. [Up/Download](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/intermediate/example1) -- This example shows how to upload files to analyze (e.g. a catalog) and download useful outputs (e.g. a plot or a table).

2. [Remote data](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/intermediate/example2) -- This example shows how to get data from a remote database, such as S3.

3. [TAP queries](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/intermediate/example3) -- This example shows how to access data via TAP/VO from an external database and use it in REANA.

### Advanced

1. [Using Notebooks](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/advanced/example1) -- This eaxmple shows how to use a Jupyter Notebook insted of a python script for the analysis.

2. [Create custom images](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/advanced/example2) -- This example shows how to build a custom imgage on gitlab, so that you can choose all the packages and libraries needed for the analsis to run.

3. [Dimensionality reduction](https://gitlab-p4n.aip.de/p4nreana/tutorials/-/tree/main/advanced/example3) -- This example shows three different projections for dimensionality reduction (UMAP, PCA, and t-SNE) and describes how to manage data flow between different pipelines using S3 private storage.

## Other Examples

There are many other examples on [REANA Hub](https://github.com/reanahub), e.g.:
- TBD (buttons)

More useful examples:
- TBD

## Useful links

- [REANA home page](http://www.reana.io/)
- [REANA documentation](http://docs.reana.io/)
- [REANA on DockerHub](https://hub.docker.com/u/reanahub/)
- [Git Basics](https://gitlab-p4n.aip.de/p4nreana/tutorial2023/-/tree/main/useful_docs/git?ref_type=heads)
