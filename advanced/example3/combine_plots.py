import os
import argparse
from minio import Minio
from PIL import Image

# S3 configuration
client = Minio(endpoint = 's3.data.aip.de:9000',
               access_key = os.environ['access_key'],
               secret_key = os.environ['secret_key'])

# Get n_test and user_folder parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--user_folder', type=str)
parser.add_argument('-n', '--number_of_tests', type=int)
out_dir = parser.parse_args().user_folder
n_test = parser.parse_args().number_of_tests

# Get the images from S3
bucket = 'reana-tutorial'
for i in range(n_test):
    file_remote = f'{out_dir}/projections_comparison_{str(i+1)}.png'
    file_local = f'./results/projections_comparison_{str(i+1)}.png'
    client.fget_object(bucket, file_remote, file_local)

# Combine plots #
im = {}
imagelist = []

for i in range(n_test):
    im[i+1] = Image.open(f'./results/projections_comparison_{str(i+1)}.png').convert('RGB')
    imagelist.append(im[i+1])

im[1].save(r'./results/merged_plots.pdf', save_all=True, append_images=imagelist[1:])
