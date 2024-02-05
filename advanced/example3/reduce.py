import os
import argparse
import pyvo as vo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import umap
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler

from minio import Minio

def make_projections(df, n_components, n_random):
    
    proj = {}
    
    # UMAP projection
    umap_model = umap.UMAP(n_components=n_components, random_state=n_random)
    umap_projection = umap_model.fit_transform(df)
    proj['UMAP'] = umap_projection
    print('UMAP done')

    # PCA projection
    pca_model = PCA(n_components=n_components, random_state=n_random)
    pca_projection = pca_model.fit_transform(df)
    proj['PCA'] = pca_projection
    print('PCA done')

    # t-SNE projection
    tsne_model = TSNE(n_components=n_components, random_state=n_random)
    tsne_projection = tsne_model.fit_transform(df)
    proj['t-SNE'] = tsne_projection
    print('t-SNE done')
    
    return(proj)

# S3 configuration
client = Minio(endpoint = 's3.data.aip.de:9000',
               access_key = os.environ['access_key'],
               secret_key = os.environ['secret_key'])

# Query Gaia archive
service = vo.dal.TAPService("https://gaia.aip.de/tap")

n_sources = 1000
query = f"""SELECT TOP {n_sources} sh.*, g.ra, g.dec, g.parallax, g.pmra, g.pmdec
            FROM gaiaedr3.gaia_source AS g
            JOIN gaiaedr3_contrib.starhorse AS sh
            USING (source_id)"""

result = service.search(query)
print('Gaia query done!\n')

# Save to DB and select columns
df_sh = result.to_table().to_pandas()
sel_cols = ['xgal', 'ygal','zgal','bprp0','mg0','parallax','pmra', 'pmdec']
df = df_sh[sel_cols].dropna()

# Loop with different random seeds

# Get n_test and user_folder parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--user_folder', type=str)
parser.add_argument('-n', '--number_of_tests', type=int)
out_dir = parser.parse_args().user_folder
n_test = parser.parse_args().number_of_tests

for i,n in enumerate(np.random.randint(10,1000,n_test)):

    print('\nRandom seed =', n)    
    proj = make_projections(df, n_components=2, n_random=n)
                
    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Scale the values for better colors
    scaler = MinMaxScaler()
    scaled = {}
	
    for j,p in enumerate(['UMAP', 'PCA', 't-SNE']):
        
        ax = axes[j]
        
        scaled[p] = scaler.fit_transform(proj[p][:, 0].reshape(-1, 1))
        ax.scatter(proj[p][:, 0], proj[p][:, 1], c=scaled[p][:, 0], cmap='viridis',label='Random seed ='+str(n))
        
        ax.set_title(f'{p} Projection')
        ax.set_xlabel(f'{p} Dimension 1')
        ax.set_ylabel(f'{p} Dimension 2')
        cbar0 = fig.colorbar(axes[0].collections[0], ax=ax)
        cbar0.set_label(f'Scaled {p} Dimension 1')
        ax.legend(loc='upper left', handlelength=0, handletextpad=0)
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plot_out = f'./results/projections_comparison_{str(i+1)}.png'
    plt.savefig(plot_out)
    
    # Uploading to S3
    client.fput_object('reana-tutorial', f'{out_dir}/projections_comparison_{str(i+1)}.png', plot_out)
    print(f'Succesfully uploaded projections_comparison_{str(i+1)}.png to S3!')
    os.remove(plot_out)
