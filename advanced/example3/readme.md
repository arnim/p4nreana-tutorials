# Theory of Dimensionality reduction

We show here 3 different alogithms to perform dimensionality reduction and describe how to manage data flow between different pipelines using S3 private storage, all through REANA.
 
### UMAP (Uniform Manifold Approximation and Projection):

**Pros:**
- Preservation of Local and Global Structure
- Scalability
- Fewer Hyperparameters

**Cons:**
- Sensitivity to Hyperparameters
- Interpretability Challenges

### t-SNE (t-distributed Stochastic Neighbor Embedding):

**Pros:**
- Preservation of Local Structure
- Visualization Quality

**Cons:**
- Computational Intensity
- Non-deterministic
- Crowding Problem

### PCA (Principal Component Analysis):

**Pros:**
- Computational Efficiency
- Interpretability
- Linear Technique

**Cons:**
- Assumption of Linearity
- Limited for Complex Structures
- Variance-Based Approach

# Unsupervised Machine learning workflow elements
* Get the N-dimentional data
* Fix parameters if possible  
* Project data with different algorithms: **t-SNE**, **UMAP**, **PCA**
* plot them side by side 
* upload results to S3
* download from S3 previous plots if exists
* combine into one grid plot to pdf 

# Data management 
This example is describing how to manage the data between different pipelines using S3 private storage.
The data round trip is following:
* download data from remote TAP service
* analyze it and plot the results
* save and upload to S3
* download if plots exists
* combine them and upload to S3

# Requirements
* access to **s3.data.aip.de** storage: 
  * **S3_ACCESS_KEY** and **S3_SECRET_KEY**
* data access to remote **TAP** service
  * we use public datasets from **gaia.aip.de** 

# Keys and secrets management
Before running the example, we need to use [**reana-client secrets**](https://docs.reana.io/reference/reana-client-cli-api/#secret-management-commands) management to store the keys to access the private folder where we want to put our results.  
Run in the terminal these two commands:

`reana-client secrets-add --env access_key=XXX`  
`reana-client secrets-add --env secret_key=XXX`

(Replace XXX with the keys that will be shared during the Tutorial.)

In this way, we can use the added keys as environment variables in our code, by simply calling, e.g., `os.environ['access_key']`. These will be used to access a private folder on S3 storage.

# Running the example on REANA

The **reana.yaml** file for this example is quite simple and made of 2 steps:
- `make-projections` runs the 3 projections for a number of times specified by the `n_test` parameter and uploads the results to S3;
- `combine-plots` retrieves all the plots from the `user_folder` and combines them in a single pdf file.  

Please change `new_user` to a customized name so you'll have your own folder inside scratch.

```
inputs:
  files:
    - reduce.py
    - combine_plots.py
  parameters:
    user_folder: new_user
    n_test: 5
workflow:
  type: serial
  specification:
    steps:
      - name: make-projections
        environment: 'gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro-ml.10134'
        commands:
          - mkdir -p results
          - python reduce.py -d ${user_folder} -n ${n_test}
      - name: combine-plots
        environment: 'gitlab-p4n.aip.de:5005/p4nreana/reana-env:py311-astro-ml.10134'
        commands:
          - python combine_plots.py -d ${user_folder} -n ${n_test}
outputs:
  files:
    - results/merged_plots.pdf
```
