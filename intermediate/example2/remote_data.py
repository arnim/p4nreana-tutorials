from io import StringIO
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u

# Load remote public data
# First 10 files from StarHorse DB
# See also: https://data.aip.de/projects/starhorse2021.html

filelist = []
for n in range(10):
    remote_data = f"https://s3.data.aip.de:9000/sh21pdf/gaiaedr3_sh_input_healpixlevel5_hpno-00000{str(n)}.fits.hdf5.txt"
    filelist.append(remote_data)

# Create big pandas dataframe
df_list = [pd.read_csv(StringIO(requests.get(file).content.decode('utf-8')),delimiter="\s+",dtype={'#ID': 'int64'}).rename(columns={"#ID": "ID"}) for file in filelist]
dfsh = pd.concat(df_list)

# Read coordinate columns in astropy framework
coords = SkyCoord(l=dfsh.glon.values, b=dfsh.glat.values, unit='degree', frame='galactic')

# Make a galactic plot in aitoff projection
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='aitoff')
l = coords.l.wrap_at(180*u.deg).radian
b = coords.b.radian
ax.hexbin(l, b, cmap=plt.cm.viridis, bins='log', gridsize = 200)
ax.set_xlabel('$\mathscr{l}$', fontsize=20)
ax.set_ylabel('$\mathscr{b}$', fontsize=20)
ax.grid(True)
fig.tight_layout()
plt.savefig('results/galactic_plot.png', format='png', dpi=150)
