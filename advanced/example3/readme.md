# Theory of dimentionality reduction
 
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
* we use **reana-client secrets** management
